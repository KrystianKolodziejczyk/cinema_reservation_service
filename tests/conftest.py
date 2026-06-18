import pytest
from httpx import ASGITransport, AsyncClient
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.modules.shared.config.settings import Settings

test_settings = Settings(_env_file=".env.test")

from app.main import app  # noqa: E402
from app.modules.shared.database_conn.base_orm import Base  # noqa: E402
from app.modules.shared.database_conn.database_client import get_session  # noqa: E402
from app.modules.shared.database_conn.redis_client import get_redis_client  # noqa: E402

test_redis_client = Redis(
    host=test_settings.redis_host,
    port=test_settings.redis_port,
    decode_responses=True,
)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def engine():
    test_engine = create_async_engine(test_settings.database_url)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield test_engine
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture
async def db_session(engine):
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    session = session_factory()
    await session.begin()
    yield session
    await session.rollback()
    await session.close()


@pytest.fixture
async def client(db_session):
    async def _override_get_session():
        yield db_session

    def _override_get_redis_client() -> Redis:
        return test_redis_client

    test_redis_client.flushdb()
    app.dependency_overrides[get_session] = _override_get_session
    app.dependency_overrides[get_redis_client] = _override_get_redis_client
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", follow_redirects=True) as ac:
        yield ac
    app.dependency_overrides.clear()
