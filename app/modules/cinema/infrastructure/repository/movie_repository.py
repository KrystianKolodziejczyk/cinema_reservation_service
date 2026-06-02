from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.domain.entities import Movie
from app.modules.cinema.infrastructure.interface import IMovieRepository
from app.modules.cinema.infrastructure.mappers import MovieMapper
from app.modules.cinema.infrastructure.orm import MovieORM


class MovieRepository(IMovieRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_movies(
        self, genre: str | None = None, title: str | None = None
    ) -> list[Movie]:
        stmt = select(MovieORM)
        if genre:
            stmt = stmt.where(MovieORM.genre == genre)
        if title:
            stmt = stmt.where(MovieORM.title.ilike(f"%{title}%"))

        result = await self._session.scalars(stmt)

        return [MovieMapper.to_entity(movie_orm) for movie_orm in result]

    async def fetch_movie(self, movie_id: int) -> Movie | None:
        stmt = select(MovieORM).where(MovieORM.movie_id == movie_id)
        movie_orm = await self._session.scalar(stmt)

        if not movie_orm:
            return None

        return MovieMapper.to_entity(movie_orm=movie_orm)
