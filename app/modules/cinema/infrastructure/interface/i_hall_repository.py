from abc import abstractmethod

from app.modules.cinema.domain.entities import Hall
from app.modules.cinema.domain.entities.seat import Seat


class IHallRepository:
    @abstractmethod
    async def create_hall(self, hall: Hall) -> int: ...

    @abstractmethod
    async def fill_hall(self, seats: list[Seat]) -> None: ...

    @abstractmethod
    async def delete_hall(self, hall_id: int) -> None: ...
