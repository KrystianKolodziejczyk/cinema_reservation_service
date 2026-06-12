from abc import ABC, abstractmethod

from app.modules.cinema.application.dto import SeatHoldData
from app.modules.cinema.domain.entities import Reservation


class IReservationRepository(ABC):
    @abstractmethod
    async def save_reservation(self, reservation: Reservation) -> int: ...

    @abstractmethod
    async def save_reserved_seats(
        self, seats: list[SeatHoldData], reservation_id: int
    ) -> None: ...
