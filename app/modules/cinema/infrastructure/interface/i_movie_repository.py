from abc import ABC, abstractmethod

from app.modules.cinema.domain.entities import Movie


class IMovieRepository(ABC):
    @abstractmethod
    async def fetch_movies(
        self, genre: str | None = None, title: str | None = None
    ) -> list[Movie]: ...

    @abstractmethod
    async def fetch_movie(self, movie_id: int) -> Movie | None: ...
