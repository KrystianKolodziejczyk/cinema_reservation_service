from collections.abc import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

url_object = URL.create(
    "postgresql+asyncpg",
    username="user",
    password="pass",
    host="localhost",
    port=8000,
    database="cinema_database",
)

engine = create_async_engine(url=url_object, echo=True)

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
