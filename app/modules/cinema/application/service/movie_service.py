from app.modules.cinema.application.interface import IMovieService


class MovieService(IMovieService):
    def __init__(self, repository) -> None:
        self._repository = repository

    async def get_movies(
        self, genre: str | None = None, search: str | None = None
    ) -> dict[str, list[str | int] | int]:
        pass
