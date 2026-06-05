from datetime import date

from app.modules.cinema.application.dto import ScreeningDetailsDTO
from app.modules.cinema.application.excpetions import (
    MovieNotFoundError,
    ScreeningNotFoundError,
)
from app.modules.cinema.application.interface import IMovieService
from app.modules.cinema.domain.entities.movie import Movie
from app.modules.cinema.infrastructure.interface import IMovieRepository


class MovieService(IMovieService):
    def __init__(self, repository: IMovieRepository) -> None:
        self._repository = repository

    async def get_movies(
        self, genre: str | None = None, title: str | None = None
    ) -> list[Movie]:
        return await self._repository.fetch_movies(genre=genre, title=title)

    async def get_movie(self, movie_id: int) -> Movie:
        result = await self._repository.fetch_movie(movie_id=movie_id)

        if not result:
            raise MovieNotFoundError(status_code=404, detail="Movie not found")

        return result

    async def get_screenings_for_movie(
        self, movie_id: int, date: date | None
    ) -> list[ScreeningDetailsDTO]:
        screenings = await self._repository.fetch_screening_for_movie(
            movie_id=movie_id, date=date
        )

        if not screenings:
            raise ScreeningNotFoundError(
                status_code=404, detail="Screening not found. Wrong movie_id or date"
            )

        return screenings
