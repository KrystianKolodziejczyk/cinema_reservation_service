import pytest

from app.modules.cinema.domain.entities import Hall, Seat
from app.modules.cinema.infrastructure.interface import IHallRepository

pytestmark = pytest.mark.anyio


class TestHallRepository:
    async def test_create_hall_returns_id(self, hall_repository: IHallRepository):
        hall = Hall(hall_id=None, hall_name="Hall A", rows=5, seats_per_row=10)

        hall_id = await hall_repository.create_hall(hall=hall)

        assert isinstance(hall_id, int)
        assert hall_id > 0

    async def test_fill_hall_creates_seats(self, hall_repository: IHallRepository):
        hall = Hall(hall_id=None, hall_name="Hall B", rows=3, seats_per_row=4)
        hall_id = await hall_repository.create_hall(hall=hall)

        seat_ids_before = await hall_repository.fetch_seat_ids(hall_id=hall_id)
        assert len(seat_ids_before) == 0

        seats = [
            Seat(seat_id=None, hall_id=hall_id, row=r, number=n, seat_type="normal")
            for r in range(1, 4)
            for n in range(1, 5)
        ]
        await hall_repository.fill_hall(seats=seats)

        seat_ids = await hall_repository.fetch_seat_ids(hall_id=hall_id)
        assert len(seat_ids) == 12

    async def test_delete_hall_returns_true(self, hall_repository: IHallRepository):
        hall = Hall(hall_id=None, hall_name="Hall C", rows=2, seats_per_row=5)
        hall_id = await hall_repository.create_hall(hall=hall)

        result = await hall_repository.delete_hall(hall_id=hall_id)

        assert result is True

    async def test_delete_hall_returns_false_when_not_found(
        self, hall_repository: IHallRepository
    ):
        result = await hall_repository.delete_hall(hall_id=99999)

        assert result is False
