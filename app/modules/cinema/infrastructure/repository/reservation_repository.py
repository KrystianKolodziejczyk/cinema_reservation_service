from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.domain.entities import Reservation
from app.modules.cinema.infrastructure.interface import IReservationRepository
from app.modules.cinema.infrastructure.mappers.reservation_mapper import (
    ReservationMapper,
)


class ReservationRepository(IReservationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_reservation(self, reservation: Reservation) -> None:
        reservation_orm = ReservationMapper.to_orm(reservation=reservation)
        self._session.add(reservation_orm)
        await self._session.flush()
