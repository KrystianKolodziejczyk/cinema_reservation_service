from dataclasses import asdict

from sqlalchemy.exc import IntegrityError

from app.modules.cinema.application.dto import (
    AddScreeningDTO,
    ScreeningDetailsDTO,
    UpdateScreeningDTO,
)
from app.modules.cinema.application.excpetions import (
    HallNotFoundError,
    MovieNotFoundError,
    PermissionDeniedError,
    ScreeningNotFoundError,
)
from app.modules.cinema.application.interface import IScreeningService
from app.modules.cinema.domain.entities import Screening
from app.modules.cinema.infrastructure.interface import IScreeningRepository


class ScreeningService(IScreeningService):
    def __init__(self, repository: IScreeningRepository) -> None:
        self._repository = repository

    def _user_role_check(self, user_role: str) -> None:
        if user_role != "admin":
            raise PermissionDeniedError(status_code=403, detail="Permision denied")

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

    async def delete_screening(self, screening_id: int, user_role: str) -> None:
        self._user_role_check(user_role)

        result = await self._repository.delete_screening(screening_id)

        if not result:
            raise ScreeningNotFoundError(
                status_code=404, detail="Screening does not exist"
            )

    async def update_screening(
        self, screening_id: int, dto: UpdateScreeningDTO, user_role: str
    ) -> None:
        self._user_role_check(user_role)
        screening = await self._repository.fetch_screening(screening_id=screening_id)
        screening.update_fields(**asdict(dto))

        try:
            await self._repository.save_screening(screening=screening)
        except IntegrityError as e:
            if "movie_id" in str(e.orig):
                raise MovieNotFoundError(
                    status_code=404, detail="Movie not found"
                ) from e
            elif "hall_id" in str(e.orig):
                raise HallNotFoundError(status_code=404, detail="Hall not found") from e

    async def get_screening(self, screening_id: int) -> ScreeningDetailsDTO:
        return await self._repository.fetch_screening_with_relations(
            screening_id=screening_id
        )
