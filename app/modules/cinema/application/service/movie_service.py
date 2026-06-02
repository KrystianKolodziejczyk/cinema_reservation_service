from app.modules.cinema.application.excpetions import MovieNotFoundError
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
