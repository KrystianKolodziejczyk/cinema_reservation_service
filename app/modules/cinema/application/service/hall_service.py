from collections.abc import Sequence
from dataclasses import asdict

from app.modules.cinema.application.dto import AddHallDTO
from app.modules.cinema.application.excpetions import (
    HallNotFoundError,
    PermissionDeniedError,
)
from app.modules.cinema.application.interface import IHallService
from app.modules.cinema.domain.entities import Hall, Seat
from app.modules.cinema.infrastructure.interface import IHallRepository


class HallService(IHallService):
    def __init__(self, repository: IHallRepository) -> None:
        self._repository = repository

    def _user_role_check(self, user_role: str) -> None:
        if user_role != "admin":
            raise PermissionDeniedError(status_code=403, detail="Permission denied")

    def _fill_hall(
        self, hall_rows: int, seats_per_row: int, hall_id: int
    ) -> Sequence[Seat]:
        hall_seats = []

        for i in range(1, hall_rows + 1):
            hall_seats.extend(
                [
                    Seat(
                        seat_id=None,
                        hall_id=hall_id,
                        row=i,
                        number=j,
                        seat_type="normal" if i < hall_rows else "vip",
                    )
                    for j in range(1, seats_per_row + 1)
                ]
            )

        return hall_seats

    async def add_hall(self, dto: AddHallDTO, user_role: str) -> int:
        self._user_role_check(user_role=user_role)

        hall = Hall(hall_id=None, **asdict(dto))

        hall_id = await self._repository.create_hall(hall=hall)

        hall_seats = self._fill_hall(
            hall_rows=hall.rows, seats_per_row=hall.seats_per_row, hall_id=hall_id
        )

        await self._repository.fill_hall(seats=hall_seats)

        return hall_id

    async def delete_hall(self, hall_id: int, user_role: str) -> None:
        self._user_role_check(user_role=user_role)

        result = await self._repository.delete_hall(hall_id=hall_id)

        if not result:
            raise HallNotFoundError(status_code=404, detail="Hall does not exist")
