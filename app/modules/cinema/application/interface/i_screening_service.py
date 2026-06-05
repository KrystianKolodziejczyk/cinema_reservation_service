from abc import ABC, abstractmethod

from app.modules.cinema.application.dto import AddScreeningDTO


class IScreeningService(ABC):
    @abstractmethod
    async def add_screening(self, dto: AddScreeningDTO, user_role: str) -> None: ...
