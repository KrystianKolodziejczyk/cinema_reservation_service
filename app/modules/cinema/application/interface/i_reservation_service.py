from abc import ABC, abstractmethod

from app.modules.cinema.application.dto import CreateReservationDTO


class IReservationService(ABC):
    @abstractmethod
    async def create_reservation(
        self, user_id: int, dto: CreateReservationDTO
    ) -> None: ...
