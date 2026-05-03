import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.main import Base
from app.dependencies import get_db_session, get_settings
from app.main import app
from app.settings import Settings

TEST_DB_URL = "sqlite+aiosqlite:///test.db"

_engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
_session_maker = async_sessionmaker(_engine, expire_on_commit=False)


async def override_get_db_session():
    async with _session_maker() as session:
        yield session


def override_get_settings():
    return Settings(db_url=TEST_DB_URL)


@pytest_asyncio.fixture(loop_scope="session", scope="session", autouse=True)
async def setup_database():
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app.dependency_overrides[get_settings] = override_get_settings
    app.dependency_overrides[get_db_session] = override_get_db_session

    yield

    app.dependency_overrides = {}

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await _engine.dispose()


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def db_session():
    async with _session_maker() as session:
        yield session
