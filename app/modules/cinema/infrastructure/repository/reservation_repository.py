from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.application.dto import SeatHoldData
from app.modules.cinema.domain.entities import Reservation
from app.modules.cinema.infrastructure.interface import IReservationRepository
from app.modules.cinema.infrastructure.mappers.reservation_mapper import (
    ReservationMapper,
)
from app.modules.cinema.infrastructure.orm import ReservedSeatORM


class ReservationRepository(IReservationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_reservation(self, reservation: Reservation) -> int:
        reservation_orm = ReservationMapper.to_orm(reservation=reservation)
        self._session.add(reservation_orm)
        await self._session.flush()

        return reservation_orm.reservation_id

    async def save_reserved_seats(
        self, seats: list[SeatHoldData], reservation_id: int
    ) -> None:
        reserved_seats_orm = [
            ReservedSeatORM(
                seat_id=seat.seat_id,
                reservation_id=reservation_id,
                price_paid=seat.price,
            )
            for seat in seats
        ]

        self._session.add_all(reserved_seats_orm)
        await self._session.flush()
