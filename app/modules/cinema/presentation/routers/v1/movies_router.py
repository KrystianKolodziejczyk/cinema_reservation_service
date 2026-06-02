from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.modules.cinema.application.interface import IMovieService
from app.modules.cinema.presentation.dependencies.movie_deps import get_movie_service
from app.modules.cinema.presentation.schemas.responses import GetMoviesResponse
from app.modules.cinema.presentation.schemas.responses.one_movie_response import (
    OneMovieResponse,
)

router = APIRouter(prefix="/v1/movies")


# ==================


@router.get("/", status_code=status.HTTP_200_OK, response_model=GetMoviesResponse)
async def get_movies(
    service: Annotated[IMovieService, Depends(get_movie_service)],
    genre: Annotated[str, Query()] | None = None,
    search: Annotated[str, Query()] | None = None,
) -> GetMoviesResponse:
    movies = await service.get_movies(genre=genre, title=search)
    return GetMoviesResponse(items=movies)


@router.get(
    "/{movie_id}", status_code=status.HTTP_200_OK, response_model=OneMovieResponse
)
async def get_movie(
    movie_id: Annotated[int, Path(gt=0)],
    service: Annotated[IMovieService, Depends(get_movie_service)],
) -> OneMovieResponse:
    movie = await service.get_movie(movie_id=movie_id)

    return OneMovieResponse(**asdict(movie))
