from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.cinema.application.dto import GetReservationDTO, SeatHoldData
from app.modules.cinema.domain.entities import Reservation, Screening
from app.modules.cinema.domain.entities.seat import Seat
from app.modules.cinema.infrastructure.interface import IReservationRepository
from app.modules.cinema.infrastructure.mappers import (
    ReservationMapper,
)
from app.modules.cinema.infrastructure.orm import (
    ReservationORM,
    ReservedSeatORM,
)


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

    async def fetch_reservation(self, reservation_id: int) -> GetReservationDTO | None:
        stmt = (
            select(ReservationORM)
            .where(ReservationORM.reservation_id == reservation_id)
            .options(
                selectinload(ReservationORM.reserved_seats).selectinload(
                    ReservedSeatORM.seat
                ),
                selectinload(ReservationORM.screening),
            )
        )

        reservation_orm = await self._session.scalar(stmt)

        if reservation_orm is None:
            return None

        return GetReservationDTO(
            reservation_id=reservation_orm.reservation_id,
            user_id=reservation_orm.user_id,
            status=reservation_orm.status,
            total_price=reservation_orm.total_price,
            conf_code=reservation_orm.conf_code,
            screening=Screening(
                screening_id=reservation_orm.screening.screening_id,
                movie_id=reservation_orm.screening.movie_id,
                hall_id=reservation_orm.screening.hall_id,
                starts_at=reservation_orm.screening.starts_at,
                price_normal=reservation_orm.screening.price_normal,
                price_vip=reservation_orm.screening.price_vip,
                status=reservation_orm.screening.status,
            ),
            seats=[
                Seat(
                    seat_id=rs.seat.seat_id,
                    hall_id=rs.seat.hall_id,
                    row=rs.seat.row,
                    number=rs.seat.number,
                    seat_type=rs.seat.seat_type,
                )
                for rs in reservation_orm.reserved_seats
            ],
        )

    async def change_reservation_status(
        self, reservation_id: int, user_id: int | None
    ) -> bool:
        stmt = update(ReservationORM)

        if not user_id:
            stmt = stmt.where(
                ReservationORM.reservation_id == reservation_id,
            )

        else:
            stmt = stmt.where(
                ReservationORM.reservation_id == reservation_id,
                ReservationORM.user_id == user_id,
            )

        stmt = stmt.values(_status="cancelled").returning(ReservationORM.reservation_id)

        reservation_id = await self._session.scalar(stmt)

        return bool(reservation_id)
