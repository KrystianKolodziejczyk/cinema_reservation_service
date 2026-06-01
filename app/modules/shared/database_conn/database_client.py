from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import app.modules.auth.infrastructure.orm  # noqa
import app.modules.cinema.infrastructure.orm  # noqa
from app.modules.shared.config.settings import settings
from app.modules.shared.database_conn.base_orm import Base

engine = create_async_engine(url=settings.database_url, echo=True)

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session, session.begin():
        yield session


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
