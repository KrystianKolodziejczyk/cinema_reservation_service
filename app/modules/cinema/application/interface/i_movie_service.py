from abc import ABC, abstractmethod
from datetime import date

from app.modules.cinema.application.dto import AddMovieDTO, ScreeningDetailsDTO
from app.modules.cinema.domain.entities.movie import Movie


class IMovieService(ABC):
    @abstractmethod
    async def get_movies(
        self, genre: str | None = None, title: str | None = None
    ) -> list[Movie]: ...

    @abstractmethod
    async def get_movie(self, movie_id: int) -> Movie: ...

    @abstractmethod
    async def get_screenings_for_movie(
        self, movie_id: int, date: date | None
    ) -> list[ScreeningDetailsDTO]: ...

    @abstractmethod
    async def add_movie(self, dto: AddMovieDTO, user_role: str) -> None: ...

    @abstractmethod
    async def delete_movie(self, movie_id: int, user_role: str) -> None: ...
