import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

from src.core.config import settings
from src.infrastructure.sqlite.database import Base
from src.infrastructure.sqlite.models import *  # noqa

config = context.config

CREATE_SCHEMA_QUERY = f'CREATE SCHEMA IF NOT EXISTS {settings.POSTGRES_SCHEMA};'

target_metadata = Base.metadata

config.set_main_option('sqlalchemy.url', settings.postgres_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def filter_foreign_schemas(name, type_, parent_names):
    return type_ != 'schema' or name == settings.POSTGRES_SCHEMA


def run_migrations_offline() -> None:
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        version_table_schema=settings.POSTGRES_SCHEMA,
        include_schemas=True,
        include_name=filter_foreign_schemas,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema=settings.POSTGRES_SCHEMA,
        include_schemas=True,
        include_name=filter_foreign_schemas,
    )

    with context.begin_transaction():
        context.execute(CREATE_SCHEMA_QUERY)
        context.run_migrations()


async def run_migrations_online(engine: AsyncEngine) -> None:
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
            future=True,
        ),
    )

    asyncio.run(run_migrations_online(connectable))
