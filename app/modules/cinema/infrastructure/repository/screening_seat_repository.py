from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.domain.entities.screening_seat import ScreeningSeat
from app.modules.cinema.infrastructure.interface import IScreeningSeatRepository
from app.modules.cinema.infrastructure.mappers import ScreeningSeatMapper


class ScreeningSeatRepository(IScreeningSeatRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_screening_seats(
        self, screening_seats: list[ScreeningSeat]
    ) -> None:
        screening_seats_orm = [
            ScreeningSeatMapper.to_orm(screening_seat)
            for screening_seat in screening_seats
        ]

        self._session.add_all(screening_seats_orm)
        await self._session.flush()
