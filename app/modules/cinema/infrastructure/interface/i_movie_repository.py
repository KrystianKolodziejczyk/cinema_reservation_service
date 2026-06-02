from abc import ABC, abstractmethod

from app.modules.cinema.domain.entities import Movie


class IMovieRepository(ABC):
    @abstractmethod
    async def get_movies(
        self, genre: str | None = None, title: str | None = None
    ) -> list[Movie]: ...
