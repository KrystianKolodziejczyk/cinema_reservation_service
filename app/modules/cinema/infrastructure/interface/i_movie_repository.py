from abc import ABC, abstractmethod
from datetime import date

from app.modules.cinema.application.dto import ScreeningDetailsDTO
from app.modules.cinema.domain.entities import Movie


class IMovieRepository(ABC):
    @abstractmethod
    async def fetch_movies(
        self,
        genre: str | None = None,
        title: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Movie], int]: ...

    @abstractmethod
    async def fetch_movie(self, movie_id: int) -> Movie | None: ...

    @abstractmethod
    async def fetch_screening_for_movie(
        self, movie_id: int, date: date | None
    ) -> list[ScreeningDetailsDTO] | None: ...

    @abstractmethod
    async def create_movie(self, movie: Movie) -> int: ...

    @abstractmethod
    async def delete_movie(self, movie_id: int) -> bool: ...
