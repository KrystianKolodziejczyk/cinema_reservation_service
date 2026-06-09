from abc import ABC, abstractmethod
from datetime import datetime

from app.modules.cinema.application.dto import SeatHoldData


class IReservationHoldRepository(ABC):
    @abstractmethod
    async def hold(
        self,
        user_id: int,
        seat_ids: list[int],
        screening_id: int,
        seats_data: list[SeatHoldData],
    ) -> tuple[int, datetime]: ...

    @abstractmethod
    async def release(self, hold_id: int, user_id: int, screening_id: int) -> bool: ...

    @abstractmethod
    async def are_seats_held(
        self, screening_id: int, seat_ids: list[int]
    ) -> list[int]: ...
