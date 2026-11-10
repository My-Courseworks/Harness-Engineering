"""Manage the operations database. Run from the ``my_multi_agent`` directory:

    python -m data_setup upgrade          # create or migrate the schema (backs up first)
    python -m data_setup seed             # load sample data into an empty database
    python -m data_setup reset --yes      # delete the database, after backing it up

The schema only ever changes through Alembic revisions in ``migrations/``.
"""

from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

from alembic import command

from commons.db import alembic_config, current_revision, database_path, head_revision

from .config import SeedConfig
from .seeding import SeedError, seed_database


def back_up(db_path: Path) -> Path | None:
    """Copy the database into ``backups/`` beside it, using SQLite's own backup API so the
    copy is consistent even if something has the file open. Returns None if there is nothing to copy."""
    if not db_path.exists() or db_path.stat().st_size == 0:
        return None
    backup_dir = db_path.parent / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    target = backup_dir / f"{db_path.stem}-{datetime.now():%Y%m%d-%H%M%S}{db_path.suffix}"
    source, destination = sqlite3.connect(db_path), sqlite3.connect(target)
    try:
        source.backup(destination)
    finally:
        source.close()
        destination.close()
    return target


def upgrade(_args: argparse.Namespace) -> int:
    db_path = database_path()
    before, head = current_revision(), head_revision()
    if before == head:
        print(f"{db_path} is already at revision {head}. Nothing to do.")
        return 0
    backup = back_up(db_path)
    if backup:
        print(f"Backed up to {backup}")
    command.upgrade(alembic_config(), "head")
    print(f"Upgraded {db_path}: {before or 'empty'} -> {head}")
    return 0


def seed(args: argparse.Namespace) -> int:
    try:
        counts = seed_database(SeedConfig(seed=args.seed, n_employees=args.employees))
    except (SeedError, RuntimeError) as error:
        print(f"Not seeded: {error}")
        return 1
    print(f"Seeded {database_path()}")
    width = max(len(table) for table in counts)
    for table, count in counts.items():
        print(f"  {table:<{width}}  {count:>5}")
    return 0


def reset(args: argparse.Namespace) -> int:
    db_path = database_path()
    if not db_path.exists():
        print(f"{db_path} does not exist. Nothing to reset.")
        return 0
    if not args.yes:
        print(f"This deletes {db_path} and everything in it. Re-run with --yes to confirm.")
        return 1
    backup = back_up(db_path)
    db_path.unlink()
    print(f"Deleted {db_path}" + (f" (backup: {backup})" if backup else ""))
    print("Next: python -m data_setup upgrade && python -m data_setup seed")
    return 0


def main(argv: list[str] | None = None) -> int:
    defaults = SeedConfig()
    parser = argparse.ArgumentParser(prog="python -m data_setup", description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("upgrade", help="create or migrate the schema to the latest revision").set_defaults(run=upgrade)

    seed_parser = commands.add_parser("seed", help="load sample data into an empty database")
    seed_parser.add_argument("--seed", type=int, default=defaults.seed, help="random seed")
    seed_parser.add_argument("--employees", type=int, default=defaults.n_employees, help="employee count")
    seed_parser.set_defaults(run=seed)

    reset_parser = commands.add_parser("reset", help="delete the database (the only command that does)")
    reset_parser.add_argument("--yes", action="store_true", help="confirm the deletion")
    reset_parser.set_defaults(run=reset)

    args = parser.parse_args(argv)
    return args.run(args)


if __name__ == "__main__":
    raise SystemExit(main())
