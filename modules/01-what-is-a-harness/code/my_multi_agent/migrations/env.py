"""Alembic environment: which database to migrate and which models to compare it with."""

from logging.config import fileConfig

from alembic import context

from commons.db import get_engine
from models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# The models are the source of truth; autogenerate diffs the database against them.
target_metadata = Base.metadata


def run_migrations() -> None:
    with get_engine().connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # SQLite cannot ALTER most things in place. Batch mode rebuilds the
            # table instead, which is what makes later revisions possible.
            render_as_batch=True,
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations()
