from dataclasses import asdict
from datetime import date

from app.modules.cinema.application.dto import AddMovieDTO, ScreeningDetailsDTO
from app.modules.cinema.application.excpetions import (
    MovieNotFoundError,
    PermissionDeniedError,
    ScreeningNotFoundError,
)
from app.modules.cinema.application.interface import IMovieService
from app.modules.cinema.domain.entities.movie import Movie
from app.modules.cinema.infrastructure.interface import IMovieRepository


class MovieService(IMovieService):
    def __init__(self, repository: IMovieRepository) -> None:
        self._repository = repository

    def _user_role_check(self, user_role: str) -> None:
        if user_role != "admin":
            raise PermissionDeniedError(status_code=403, detail="Permission denied")

    async def get_movies(
        self,
        genre: str | None = None,
        title: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Movie], int]:
        return await self._repository.fetch_movies(
            genre=genre, title=title, page=page, limit=limit
        )

    async def get_movie(self, movie_id: int) -> Movie:
        result = await self._repository.fetch_movie(movie_id=movie_id)

        if not result:
            raise MovieNotFoundError(status_code=404, detail="Movie not found")

        return result

    async def get_screenings_for_movie(
        self, movie_id: int, date: date | None
    ) -> list[ScreeningDetailsDTO]:
        screenings = await self._repository.fetch_screenings_for_movie(
            movie_id=movie_id, date=date
        )

        if not screenings:
            raise ScreeningNotFoundError(
                status_code=404, detail="Screening not found. Wrong movie_id or date"
            )

        return screenings

    async def add_movie(self, dto: AddMovieDTO, user_role: str) -> int:
        self._user_role_check(user_role=user_role)
        movie = Movie(movie_id=None, **asdict(dto))

        return await self._repository.create_movie(movie=movie)

    async def delete_movie(self, movie_id: int, user_role: str) -> None:
        self._user_role_check(user_role=user_role)

        result = await self._repository.delete_movie(movie_id=movie_id)

        if not result:
            raise MovieNotFoundError(status_code=404, detail="Movie not found")
