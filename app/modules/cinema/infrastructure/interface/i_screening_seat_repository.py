from abc import ABC, abstractmethod

from app.modules.cinema.domain.entities import ScreeningSeat


class IScreeningSeatRepository(ABC):
    @abstractmethod
    async def create_screening_seats(
        self, screening_seats: list[ScreeningSeat]
    ) -> None: ...
