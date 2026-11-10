"""The one place that knows where the operations database is and how to open it.

Everything else asks this module for a session. Nothing here runs at import
time: the engine is created on first use.
"""

import os
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import Iterator

from alembic.config import Config as AlembicConfig
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from commons.config import load_config

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = PROJECT_ROOT / "migrations"


def _resolve(path: str) -> Path:
    """Config paths are relative to the project root, never to the working directory."""
    candidate = Path(path).expanduser()
    return candidate if candidate.is_absolute() else PROJECT_ROOT / candidate


def database_path() -> Path:
    return _resolve(os.environ.get("OPS_DESK_DB") or load_config().database.path)


def sessions_path() -> Path:
    return _resolve(load_config().database.sessions_path)


@lru_cache(maxsize=None)
def get_engine() -> Engine:
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{path}")

    @event.listens_for(engine, "connect")
    def _enforce_foreign_keys(dbapi_connection, _record) -> None:
        # SQLite does not enforce foreign keys unless asked, per connection.
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.close()

    return engine


@contextmanager
def session_scope() -> Iterator[Session]:
    """One unit of work: commit on a clean exit, roll back on an exception.

    Objects stay readable after the block closes (expire_on_commit=False), so a
    data-access function can return what it loaded.
    """
    session = sessionmaker(get_engine(), expire_on_commit=False)()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ------------------------- schema version -------------------------

def alembic_config() -> AlembicConfig:
    """Alembic configured by absolute paths, so it works from any working directory."""
    config = AlembicConfig(str(PROJECT_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(MIGRATIONS_DIR))
    return config


def head_revision() -> str | None:
    return ScriptDirectory.from_config(alembic_config()).get_current_head()


def current_revision() -> str | None:
    """The revision recorded inside the database, or None if it has never been migrated."""
    with get_engine().connect() as connection:
        return MigrationContext.configure(connection).get_current_revision()


def require_current_schema() -> None:
    """Refuse to run against a database whose schema is not the one the code expects."""
    current, head = current_revision(), head_revision()
    if current != head:
        raise RuntimeError(
            f"The database at {database_path()} is at schema revision {current or 'none'}, "
            f"but the code expects {head}. Run: python -m data_setup upgrade"
        )
