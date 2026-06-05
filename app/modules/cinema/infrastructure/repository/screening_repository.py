from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.domain.entities import Screening
from app.modules.cinema.infrastructure.interface import IScreeningRepository
from app.modules.cinema.infrastructure.mappers import ScreeningMapper


class ScreeningRepository(IScreeningRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_screenings(self, screenings: list[Screening]) -> None:
        screenings_orm = [ScreeningMapper.to_orm(screening) for screening in screenings]

        self._session.add_all(screenings_orm)
        await self._session.flush()
