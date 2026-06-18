from unittest.mock import AsyncMock

import pytest

from app.modules.cinema.application.dto import AddMovieDTO
from app.modules.cinema.application.excpetions import (
    MovieNotFoundError,
    PermissionDeniedError,
    ScreeningNotFoundError,
)
from app.modules.cinema.application.service import MovieService

pytestmark = pytest.mark.anyio


class TestMovieServiceExceptions:
    async def test_raises_permission_denied_on_add(
        self, mock_movie_repository: AsyncMock
    ):
        service = MovieService(repository=mock_movie_repository)
        dto = AddMovieDTO(
            title="Test",
            description="Desc",
            director="Dir",
            duration=90,
            genre="drama",
            rating=4.0,
            poster_url=None,
        )

        with pytest.raises(PermissionDeniedError):
            await service.add_movie(dto=dto, user_role="client")

    async def test_raises_permission_denied_on_delete(
        self, mock_movie_repository: AsyncMock
    ):
        service = MovieService(repository=mock_movie_repository)

        with pytest.raises(PermissionDeniedError):
            await service.delete_movie(movie_id=1, user_role="client")

    async def test_raises_movie_not_found_on_get(
        self, mock_movie_repository: AsyncMock
    ):
        mock_movie_repository.fetch_movie.return_value = None
        service = MovieService(repository=mock_movie_repository)

        with pytest.raises(MovieNotFoundError):
            await service.get_movie(movie_id=99999)

    async def test_raises_movie_not_found_on_delete(
        self, mock_movie_repository: AsyncMock
    ):
        mock_movie_repository.delete_movie.return_value = False
        service = MovieService(repository=mock_movie_repository)

        with pytest.raises(MovieNotFoundError):
            await service.delete_movie(movie_id=99999, user_role="admin")

    async def test_raises_screening_not_found(self, mock_movie_repository: AsyncMock):
        mock_movie_repository.fetch_screenings_for_movie.return_value = None
        service = MovieService(repository=mock_movie_repository)

        with pytest.raises(ScreeningNotFoundError):
            await service.get_screenings_for_movie(movie_id=1, date=None)
