import asyncio

import asyncpg
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from main_service.src.app.config_db import app_config
from main_service.src.app.db.models.base import Base


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def config():
    app_config.postgres.db_name = f'{app_config.postgres.db_name}_test'
    yield app_config


@pytest_asyncio.fixture(scope='session')
async def flush_db(config):
    postgres_table_uri = f'postgresql://{app_config.postgres.url}/postgres'

    connection = await asyncpg.connect(postgres_table_uri)
    await connection.execute(f'DROP DATABASE IF EXISTS {app_config.postgres.db_name}_test' )
    await connection.execute(f'CREATE DATABASE {app_config.postgres.db_name}_test')
    await connection.close()
    yield
    connection = await asyncpg.connect(postgres_table_uri)
    await connection.execute(f'DROP DATABASE IF EXISTS {app_config.postgres.db_name}_test' )
    await connection.close()


@pytest_asyncio.fixture(scope='session')
async def db_engine(config):
    yield create_async_engine(config.postgres.uri, echo=True)


@pytest_asyncio.fixture(scope='session')
async def new_db_schema(flush_db, db_engine):
    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await db_engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def db_session(new_db_schema, db_engine):
    pg_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with pg_session() as session, session.begin():
        yield session
        await session.rollback()
        await session.close()
