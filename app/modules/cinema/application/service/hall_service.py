from dataclasses import asdict

from app.modules.cinema.application.dto import AddHallDTO
from app.modules.cinema.application.excpetions import PermissionDeniedError
from app.modules.cinema.application.interface import IHallService
from app.modules.cinema.domain.entities.hall import Hall
from app.modules.cinema.infrastructure.interface import IHallRepository


class HallService(IHallService):
    def __init__(self, repository: IHallRepository) -> None:
        self._repository = repository

    async def add_hall(self, dto: AddHallDTO, user_role: str) -> None:
        if user_role != "admin":
            raise PermissionDeniedError(status_code=403, detail="Permission denied")

        hall = Hall(hall_id=None, **asdict(dto))

        await self._repository.create_hall(hall=hall)
