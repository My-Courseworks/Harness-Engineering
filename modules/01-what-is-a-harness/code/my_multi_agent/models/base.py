"""Declarative base shared by every model.

The models are the single source of truth for the schema. Tables are never
written by hand: Alembic compares these classes with the database and
generates the migration (see ``migrations/``).
"""

from datetime import datetime, timezone

from sqlalchemy import MetaData, text
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

# Every constraint gets a deterministic name. SQLite can only alter a constraint
# by rebuilding the table, and Alembic's batch mode needs the name to find it.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# Timestamps are ISO-8601 text, UTC, minute precision, so string order is
# chronological order. The same value is produced in SQL (for rows written
# outside the ORM) and in Python (for rows written through it).
UTC_NOW_SQL = text("(strftime('%Y-%m-%dT%H:%M','now') || 'Z')")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M") + "Z"


class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    """Models are dataclasses: keyword-only construction, a readable repr, value equality."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)
