# File: PingMe_Backend/migrations/env.py

import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# --- CUSTOM IMPORTS ---
from app.db.database import Base, engine  # Your Base and async engine
from app.db import models  # Import your models file so Alembic knows about them
# ----------------------

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata to your Base
# This tells Alembic which models to track.
target_metadata = Base.metadata

# other values from the config, defined by the needs of environment.
# ... (standard variables like file_template, etc.)
def include_object(object, name, type_, reflected, compare_to):
    """Exclude objects not explicitly imported/used"""
    if type_ == "table" and object.schema != target_metadata.schema:
        return False
    return True

# Helper function that performs the actual migration work
def do_run_migrations(connection):
    """The core logic that runs the migration commands."""
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        # Uncomment the line below if you want to explicitly include/exclude tables:
        # include_object=include_object 
    )

    with context.begin_transaction():
        context.run_migrations()

# Standard synchronous run (for use when not using async engine)
def run_migrations_offline():
    """Run migrations in 'offline' mode.
    ... (Standard Alembic boilerplate, usually not changed)
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# ASYNCHRONOUS MIGRATION EXECUTION (Your required logic)
def run_migrations_online():
    """Run migrations in 'online' mode with async support."""
    # This block uses your imported 'engine' object (which is async)
    connectable = engine

    async def run_async_migrations():
        # Connect to the engine and run the sync migration function
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

        # Dispose of the connection pool after the migration
        await connectable.dispose()

    # Execute the async function
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()