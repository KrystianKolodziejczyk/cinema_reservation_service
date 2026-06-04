from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.domain.entities import Hall
from app.modules.cinema.infrastructure.interface import IHallRepository
from app.modules.cinema.infrastructure.mappers import HallMapper


class HallRepository(IHallRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_hall(self, hall: Hall) -> None:
        hall_orm = HallMapper.to_orm(hall)

        self._session.add(hall_orm)
        await self._session.flush()
