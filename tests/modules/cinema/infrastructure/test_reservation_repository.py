import pytest

from app.modules.cinema.domain.entities import Reservation, Screening
from app.modules.cinema.infrastructure.interface import IReservationRepository

pytestmark = pytest.mark.anyio


class TestReservationRepository:
    async def test_save_and_fetch_reservation(
        self,
        reservation_repository: IReservationRepository,
        db_user: int,
        db_screening: Screening,
    ):
        reservation = Reservation(
            reservation_id=None,
            user_id=db_user,
            screening_id=db_screening.screening_id,
            status="confirmed",
            total_price=25,
        )

        reservation_id = await reservation_repository.save_reservation(reservation=reservation)
        fetched = await reservation_repository.fetch_reservation(reservation_id=reservation_id)

        assert fetched is not None
        assert fetched.reservation_id == reservation_id
        assert fetched.user_id == db_user

    async def test_fetch_reservation_returns_none_when_not_found(
        self, reservation_repository: IReservationRepository
    ):
        result = await reservation_repository.fetch_reservation(reservation_id=99999)

        assert result is None

    async def test_change_reservation_status(
        self,
        reservation_repository: IReservationRepository,
        db_user: int,
        db_screening: Screening,
    ):
        reservation = Reservation(
            reservation_id=None,
            user_id=db_user,
            screening_id=db_screening.screening_id,
            status="confirmed",
            total_price=25,
        )
        reservation_id = await reservation_repository.save_reservation(reservation=reservation)

        result = await reservation_repository.change_reservation_status(
            reservation_id=reservation_id, user_id=db_user
        )

        assert result is True

    async def test_fetch_reservations_for_user(
        self,
        reservation_repository: IReservationRepository,
        db_user: int,
        db_screening: Screening,
    ):
        reservation = Reservation(
            reservation_id=None,
            user_id=db_user,
            screening_id=db_screening.screening_id,
            status="confirmed",
            total_price=25,
        )
        await reservation_repository.save_reservation(reservation=reservation)

        items, total = await reservation_repository.fetch_reservations_for_user(user_id=db_user)

        assert total == 1
        assert len(items) == 1
        assert items[0].user_id == db_user
