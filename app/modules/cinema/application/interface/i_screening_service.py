from abc import ABC, abstractmethod

from app.modules.cinema.application.dto import (
    AddScreeningDTO,
    ReservationHoldDTO,
    ScreeningDetailsDTO,
    UpdateScreeningDTO,
)


class IScreeningService(ABC):
    @abstractmethod
    async def add_screening(self, dto: AddScreeningDTO, user_role: str) -> list[int]: ...

    @abstractmethod
    async def delete_screening(self, screening_id: int, user_role: str) -> None: ...

    @abstractmethod
    async def update_screening(
        self, screening_id: int, dto: UpdateScreeningDTO, user_role: str
    ) -> None: ...

    @abstractmethod
    async def get_screening(self, screening_id: int) -> ScreeningDetailsDTO: ...

    @abstractmethod
    async def hold_seats(
        self, seat_ids: list[int], user_id: int, screening_id: int
    ) -> ReservationHoldDTO: ...

    @abstractmethod
    async def release_hold(
        self, hold_id: int, user_id: int, screening_id: int
    ) -> None: ...
