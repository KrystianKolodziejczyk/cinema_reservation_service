from typing import Annotated

from fastapi import APIRouter, Query

from app.modules.cinema.application.interface import IMovieService
from app.modules.cinema.presentation.dependencies.movie_deps import get_movie_service
from app.modules.shared.dependencies.auth_deps import get_current_user

router = APIRouter(prefix="/v1/movies")


# ==================


@router.get("/")
async def get_movies(
    user_id: Annotated[int, get_current_user()],
    service: Annotated[IMovieService, get_movie_service()],
    genre: Annotated[str, Query()] | None = None,
    search: Annotated[str, Query()] | None = None,
):
    pass
