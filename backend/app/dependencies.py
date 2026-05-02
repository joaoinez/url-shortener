from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.config import Settings
from app.db.main import create_db_engine, create_db_session_maker

# TODO: Make this a class
engine: AsyncEngine | None = None
session_maker: async_sessionmaker[AsyncSession] | None = None


@lru_cache()
def get_settings():
    return Settings()  # pyright: ignore[reportCallIssue]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global engine, session_maker

    settings = get_settings()

    engine = await create_db_engine(settings.db_url)
    session_maker = await create_db_session_maker(engine)

    yield

    if engine:
        await engine.dispose()


async def get_db_session():
    if session_maker is None:
        return

    async with session_maker() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_db_session)]
AppSettings = Annotated[Settings, Depends(get_settings)]
