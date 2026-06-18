import pytest

from app.modules.cinema.domain.entities import Movie
from app.modules.cinema.infrastructure.interface import IMovieRepository

pytestmark = pytest.mark.anyio


class TestMovieRepository:
    async def test_create_and_fetch_movie(self, movie_repository: IMovieRepository):
        movie = Movie(
            movie_id=None,
            title="Inception",
            description="A mind-bending thriller",
            director="Christopher Nolan",
            duration=148,
            genre="sci-fi",
            rating=4.8,
            poster_url=None,
        )

        movie_id = await movie_repository.create_movie(movie=movie)
        fetched = await movie_repository.fetch_movie(movie_id=movie_id)

        assert fetched is not None
        assert fetched.movie_id == movie_id
        assert fetched.title == "Inception"

    async def test_fetch_movie_returns_none_when_not_found(
        self, movie_repository: IMovieRepository
    ):
        result = await movie_repository.fetch_movie(movie_id=99999)

        assert result is None

    async def test_fetch_movies_with_genre_filter(self, movie_repository: IMovieRepository):
        movie = Movie(
            movie_id=None,
            title="The Dark Knight",
            description="A superhero film",
            director="Christopher Nolan",
            duration=152,
            genre="action",
            rating=4.9,
            poster_url=None,
        )
        await movie_repository.create_movie(movie=movie)

        movies, total = await movie_repository.fetch_movies(genre="action")

        assert total >= 1
        assert all(m.genre == "action" for m in movies)

    async def test_delete_movie_returns_true(self, movie_repository: IMovieRepository):
        movie = Movie(
            movie_id=None,
            title="Interstellar",
            description="Space exploration",
            director="Christopher Nolan",
            duration=169,
            genre="sci-fi",
            rating=4.7,
            poster_url=None,
        )
        movie_id = await movie_repository.create_movie(movie=movie)

        result = await movie_repository.delete_movie(movie_id=movie_id)

        assert result is True

    async def test_delete_movie_returns_false_when_not_found(
        self, movie_repository: IMovieRepository
    ):
        result = await movie_repository.delete_movie(movie_id=99999)

        assert result is False
