from abc import ABC, abstractmethod

from app.modules.cinema.domain.entities.movie import Movie


class IMovieService(ABC):
    @abstractmethod
    async def get_movies(
        self, genre: str | None = None, title: str | None = None
    ) -> list[Movie]: ...

    @abstractmethod
    async def get_movie(self, movie_id: int) -> Movie: ...
