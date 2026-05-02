from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


async def create_db_engine(db_url: str):
    engine = create_async_engine(
        db_url, echo=True, connect_args={"check_same_thread": False}
    )

    return engine


async def create_db_session_maker(engine: AsyncEngine):
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    return session_maker
