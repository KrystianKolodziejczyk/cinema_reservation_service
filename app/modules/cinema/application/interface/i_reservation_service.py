from abc import ABC, abstractmethod

from app.modules.cinema.application.dto import CreateReservationDTO, ReservationDTO


class IReservationService(ABC):
    @abstractmethod
    async def create_reservation(
        self, user_id: int, dto: CreateReservationDTO
    ) -> ReservationDTO: ...

    @abstractmethod
    async def get_reservation(
        self, reservation_id: int, user_data: dict[str, str | int]
    ) -> ReservationDTO: ...

    @abstractmethod
    async def cancel_reservation(
        self, reservation_id: int, user_data: dict
    ) -> None: ...

    @abstractmethod
    async def get_reservation_history(
        self, user_id: int, page: int = 1, limit: int = 20
    ) -> tuple[list[ReservationDTO | None], int]: ...
