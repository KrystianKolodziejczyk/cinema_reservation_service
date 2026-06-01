from abc import ABC, abstractmethod


class IMovieService(ABC):
    @abstractmethod
    async def get_movies(
        self, genre: str | None = None, search: str | None = None
    ) -> dict[str, list[str | int] | int]: ...
