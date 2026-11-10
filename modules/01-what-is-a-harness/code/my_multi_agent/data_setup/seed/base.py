"""The seeding abstraction.

A ``Seeder`` fills the tables of one cluster. The seeding run depends only on this interface, so a
new cluster is added by writing a new subclass and registering it, without modifying existing code.
"""

from __future__ import annotations

import random
from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any, ClassVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models import Base

from ..config import SeedConfig


@dataclass
class SeedContext:
    """Everything a seeder is handed: no globals, no hidden state.

    ``registry`` is how seeders hand ids to the seeders that run after them
    (for example, the people seeder publishes ``active_employee_ids``).
    """

    session: Session
    rng: random.Random
    config: SeedConfig
    _registry: dict[str, Any] = field(default_factory=dict)

    def add_rows(self, model: type[Base], columns: Sequence[str], rows: Iterable[Sequence[Any]]) -> None:
        """Build one ``model`` object per row and add it to the session.

        Seeders compute plain rows so their random draws stay easy to read; the objects are
        built here, which means a misspelt column fails at construction rather than in SQL.
        The rows are written straight away: seeders call this in foreign-key order, and the
        session only reorders inserts across tables for models linked by a relationship.
        """
        self.session.add_all(model(**dict(zip(columns, row))) for row in rows)
        self.session.flush()

    def count(self, model: type[Base]) -> int:
        return self.session.scalar(select(func.count()).select_from(model)) or 0

    def publish(self, key: str, value: Any) -> None:
        if key in self._registry:
            raise KeyError(f"'{key}' was already published")
        self._registry[key] = value

    def require(self, key: str) -> Any:
        if key not in self._registry:
            raise KeyError(f"'{key}' has not been published by an earlier seeder")
        return self._registry[key]

    def has(self, key: str) -> bool:
        return key in self._registry


class Seeder(ABC):
    """Template method: ``run`` checks preconditions, calls ``seed``, then checks the postcondition."""

    name: ClassVar[str]
    tables: ClassVar[tuple[type[Base], ...]]   # models this seeder is responsible for filling
    requires: ClassVar[tuple[str, ...]] = ()   # registry keys that earlier seeders must publish

    def run(self, ctx: SeedContext) -> None:
        missing = [key for key in self.requires if not ctx.has(key)]
        if missing:
            raise RuntimeError(
                f"Seeder '{self.name}' needs {missing}; register the seeder that publishes them first."
            )
        self.seed(ctx)
        empty = [model.__tablename__ for model in self.tables if ctx.count(model) == 0]
        if empty:
            raise RuntimeError(f"Seeder '{self.name}' left these tables empty: {empty}")

    @abstractmethod
    def seed(self, ctx: SeedContext) -> None:
        """Insert rows for ``self.tables`` and publish any ids later seeders need."""
