from abc import ABC, abstractmethod

from app.modules.cinema.application.dto import ReservationDTO, SeatHoldData
from app.modules.cinema.domain.entities import Reservation


class IReservationRepository(ABC):
    @abstractmethod
    async def save_reservation(self, reservation: Reservation) -> int: ...

    @abstractmethod
    async def save_reserved_seats(
        self, seats: list[SeatHoldData], reservation_id: int
    ) -> None: ...

    @abstractmethod
    async def fetch_reservation(
        self, reservation_id: int
    ) -> ReservationDTO | None: ...

    @abstractmethod
    async def change_reservation_status(
        self, reservation_id: int, user_id: int | None
    ) -> bool: ...

    @abstractmethod
    async def fetch_reservations_for_user(
        self, user_id: int, page: int = 1, limit: int = 20
    ) -> tuple[list[ReservationDTO | None], int]: ...
