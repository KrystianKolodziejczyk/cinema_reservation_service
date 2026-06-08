from abc import ABC, abstractmethod

from app.modules.cinema.application.dto import ScreeningDetailsDTO
from app.modules.cinema.domain.entities.screening import Screening


class IScreeningRepository(ABC):
    @abstractmethod
    async def create_screenings(self, screening: list[Screening]) -> None: ...

    @abstractmethod
    async def delete_screening(self, screening_id: int) -> bool: ...

    @abstractmethod
    async def fetch_basic_screening(self, screening_id: int) -> Screening: ...

    @abstractmethod
    async def save_screening(self, screening: Screening) -> None: ...

    @abstractmethod
    async def fetch_screening_with_relations(
        self, screening_id: int
    ) -> ScreeningDetailsDTO | None: ...
