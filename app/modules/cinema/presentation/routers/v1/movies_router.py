from dataclasses import asdict
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.modules.cinema.application.dto import AddMovieDTO
from app.modules.cinema.application.interface import IMovieService
from app.modules.cinema.presentation.dependencies.movie_deps import get_movie_service
from app.modules.cinema.presentation.schemas.request.add_movie_request import (
    AddMovieRequest,
)
from app.modules.cinema.presentation.schemas.responses import GetMoviesResponse
from app.modules.cinema.presentation.schemas.responses.get_screenings_response import (
    GetScreeningResponse,
)
from app.modules.cinema.presentation.schemas.responses.one_movie_response import (
    OneMovieResponse,
)
from app.modules.shared.dependencies.auth_deps import get_current_user

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


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_movie(
    body: AddMovieRequest,
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IMovieService, Depends(get_movie_service)],
):
    dto = AddMovieDTO(**body.model_dump())
    await service.add_movie(dto=dto, user_role=user_data["role"])


@router.get(
    "/{movie_id}", status_code=status.HTTP_200_OK, response_model=OneMovieResponse
)
async def get_movie(
    movie_id: Annotated[int, Path(gt=0)],
    service: Annotated[IMovieService, Depends(get_movie_service)],
) -> OneMovieResponse:
    movie = await service.get_movie(movie_id=movie_id)

    return OneMovieResponse(**asdict(movie))


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    movie_id: Annotated[int, Path(gt=0)],
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IMovieService, Depends(get_movie_service)],
) -> None:
    await service.delete_movie(movie_id=movie_id, user_role=user_data["role"])


@router.get(
    "/{movie_id}/screenings",
    status_code=status.HTTP_200_OK,
    response_model=GetScreeningResponse,
)
async def get_screenings_for_movie(
    movie_id: Annotated[int, Path(gt=0)],
    date: Annotated[date | None, Query()],
    service: Annotated[IMovieService, Depends(get_movie_service)],
) -> GetScreeningResponse:
    screenings = await service.get_screenings_for_movie(movie_id=movie_id, date=date)
    return GetScreeningResponse(**asdict(screenings))
