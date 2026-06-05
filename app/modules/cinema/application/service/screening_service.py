from sqlalchemy.exc import IntegrityError

from app.modules.cinema.application.dto.add_screening_dto import AddScreeningDTO
from app.modules.cinema.application.excpetions import (
    HallNotFoundError,
    MovieNotFoundError,
    PermissionDeniedError,
)
from app.modules.cinema.application.interface import IScreeningService
from app.modules.cinema.domain.entities import Screening
from app.modules.cinema.infrastructure.interface import IScreeningRepository


class ScreeningService(IScreeningService):
    def __init__(self, repository: IScreeningRepository) -> None:
        self._repository = repository

    def _user_role_check(self, user_role: str) -> None:
        if user_role != "admin":
            raise PermissionDeniedError(status_code=403, details="Permision denied")

    async def add_screening(self, dto: AddScreeningDTO, user_role: str) -> None:
        self._user_role_check(user_role=user_role)

        screenings = [
            Screening(
                screening_id=None,
                movie_id=dto.movie_id,
                hall_id=dto.hall_id,
                starts_at=dto.starts_at[i],
                price_normal=dto.price_normal,
                price_vip=dto.price_vip,
                status=dto.status,
            )
            for i in range(len(dto.starts_at))
        ]

        try:
            await self._repository.create_screenings(screenings=screenings)

        except IntegrityError as e:
            if "movie_id" in str(e.orig):
                raise MovieNotFoundError(
                    status_code=404, detail="Movie not found"
                ) from e
            elif "hall_id" in str(e.orig):
                raise HallNotFoundError(status_code=404, detail="Hall not found") from e
