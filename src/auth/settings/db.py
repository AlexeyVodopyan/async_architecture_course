# stdlib
from asyncio import current_task
from contextlib import asynccontextmanager

# thirdparty
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

# project
from src.auth.settings.config import settings

SQLALCHEMY_URL = URL.create(
    drivername="postgresql+asyncpg",
    host=settings.db.host,
    username=settings.db.user,
    password=settings.db.password,
    port=settings.db.port,
    database=settings.db.db,
)

engine = create_async_engine(SQLALCHEMY_URL, pool_size=20, max_overflow=0)

async_session_maker = async_scoped_session(
    async_sessionmaker(bind=engine), scopefunc=current_task
)


async def get_session():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()


@asynccontextmanager
async def get_session_cm():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()
