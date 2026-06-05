from abc import ABC, abstractmethod

from app.modules.cinema.domain.entities.screening import Screening


class IScreeningRepository(ABC):
    @abstractmethod
    async def create_screenings(self, screening: list[Screening]) -> None: ...
