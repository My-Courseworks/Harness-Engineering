"""Loads the sample data into an empty, fully migrated database."""

from __future__ import annotations

import random

from sqlalchemy import text

from commons.db import database_path, require_current_schema, session_scope
from models import Base

from .config import SeedConfig
from .seed import default_seeders
from .seed.base import SeedContext


class SeedError(RuntimeError):
    pass


def row_counts() -> dict[str, int]:
    """Rows per table, in dependency order."""
    with session_scope() as session:
        return {
            table.name: session.execute(text(f"SELECT COUNT(*) FROM {table.name}")).scalar_one()
            for table in Base.metadata.sorted_tables
        }


def seed_database(config: SeedConfig) -> dict[str, int]:
    """Seed every cluster in one transaction and return the row counts.

    Refuses to touch a database that already holds rows: seeding is for an empty
    database, never a way to overwrite one. Either every seeder succeeds and the
    foreign keys hold, or nothing is written.
    """
    require_current_schema()

    populated = {table: count for table, count in row_counts().items() if count}
    if populated:
        raise SeedError(
            f"{database_path()} already has data in: {', '.join(populated)}. "
            "Seeding only runs on an empty database. To start over on purpose: "
            "python -m data_setup reset --yes"
        )

    with session_scope() as session:
        ctx = SeedContext(session=session, rng=random.Random(config.seed), config=config)
        for seeder in default_seeders():
            seeder.run(ctx)

        violations = session.execute(text("PRAGMA foreign_key_check")).fetchall()
        if violations:
            raise SeedError(f"Foreign key violations after seeding: {violations[:5]}")

    return row_counts()
