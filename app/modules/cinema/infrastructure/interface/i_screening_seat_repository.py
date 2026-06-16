from abc import ABC, abstractmethod

from app.modules.cinema.domain.entities import ScreeningSeat


class IScreeningSeatRepository(ABC):
    @abstractmethod
    async def create_screening_seats(
        self, screening_seats: list[ScreeningSeat]
    ) -> None: ...

    @abstractmethod
    async def set_seat_as_reserved(
        self, reservation_id: int, seat_ids: list[int], screening_id: int
    ) -> None: ...

    @abstractmethod
    async def release_screening_seats(self, reservation_id: int) -> None: ...
