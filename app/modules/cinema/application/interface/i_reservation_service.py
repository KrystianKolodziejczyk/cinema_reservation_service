from abc import ABC, abstractmethod

from app.modules.cinema.application.dto import CreateReservationDTO, GetReservationDTO


class IReservationService(ABC):
    @abstractmethod
    async def create_reservation(
        self, user_id: int, dto: CreateReservationDTO
    ) -> int: ...

    @abstractmethod
    async def get_reservation(
        self, reservation_id: int, user_data: dict[str, str | int]
    ) -> GetReservationDTO: ...

    @abstractmethod
    async def cancel_reservation(
        self, reservation_id: int, user_data: dict
    ) -> None: ...
