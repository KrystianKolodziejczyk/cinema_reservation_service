from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.domain.entities.screening_seat import ScreeningSeat
from app.modules.cinema.infrastructure.interface import IScreeningSeatRepository
from app.modules.cinema.infrastructure.mappers import ScreeningSeatMapper
from app.modules.cinema.infrastructure.orm.screening_seat_orm import ScreeningSeatORM


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

    async def set_seat_as_reserved(
        self, reservation_id: int, seat_ids: list[int]
    ) -> None:
        stmt = (
            update(ScreeningSeatORM)
            .where(
                ScreeningSeatORM.reservation_id.is_(None)
                & ScreeningSeatORM.seat_id.in_(seat_ids)
            )
            .values(reservation_id=reservation_id, status="reserved")
        )

        await self._session.execute(stmt)

    async def release_screening_seats(self, reservation_id: int) -> bool:
        stmt = (
            update(ScreeningSeatORM)
            .where(ScreeningSeatORM.reservation_id == reservation_id)
            .values(reservation_id=None, status="free")
        )

        await self._session.execute(stmt)
