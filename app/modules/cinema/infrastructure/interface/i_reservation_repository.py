from abc import ABC, abstractmethod

from app.modules.cinema.domain.entities import Reservation


class IReservationRepository(ABC):
    @abstractmethod
    async def save_reservation(self, reservation: Reservation) -> None: ...
