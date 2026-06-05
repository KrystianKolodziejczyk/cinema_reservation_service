from abc import ABC, abstractmethod

from app.modules.cinema.application.dto.add_hall_dto import AddHallDTO


class IHallService(ABC):
    @abstractmethod
    async def add_hall(self, dto: AddHallDTO, user_role: str) -> None: ...

    @abstractmethod
    async def delete_hall(self, hall_id: int, user_role: str) -> None: ...
