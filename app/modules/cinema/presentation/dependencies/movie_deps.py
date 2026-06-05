from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.application.interface import IMovieService
from app.modules.cinema.application.service import MovieService
from app.modules.cinema.infrastructure.repository import MovieRepository
from app.modules.shared.database_conn.database_client import get_session


def get_movie_service(session: AsyncSession = Depends(get_session)) -> IMovieService:
    return MovieService(repository=MovieRepository(session=session))
