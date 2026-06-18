from dataclasses import asdict
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.modules.cinema.application.dto import AddMovieDTO
from app.modules.cinema.application.interface import IMovieService
from app.modules.cinema.presentation.dependencies import get_movie_service
from app.modules.cinema.presentation.schemas.request import (
    AddMovieRequest,
)
from app.modules.cinema.presentation.schemas.responses import (
    AddMovieResponse,
    MovieDetailResponse,
    MovieListResponse,
    ScreeningDetailResponse,
)
from app.modules.shared.dependencies.auth_deps import get_current_user

router = APIRouter(prefix="/v1/movies")


# ==================


@router.get("/", status_code=status.HTTP_200_OK, response_model=MovieListResponse)
async def get_movies(
    service: Annotated[IMovieService, Depends(get_movie_service)],
    genre: Annotated[str, Query()] | None = None,
    search: Annotated[str, Query()] | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> MovieListResponse:
    movies, total = await service.get_movies(genre=genre, title=search, page=page, limit=limit)
    return MovieListResponse(items=movies, total=total, page=page, limit=limit)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AddMovieResponse)
async def add_movie(
    body: AddMovieRequest,
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IMovieService, Depends(get_movie_service)],
) -> AddMovieResponse:
    dto = AddMovieDTO(**body.model_dump())
    movie_id = await service.add_movie(dto=dto, user_role=user_data["role"])
    return AddMovieResponse(movie_id=movie_id)


@router.get(
    "/{movie_id}", status_code=status.HTTP_200_OK, response_model=MovieDetailResponse
)
async def get_movie(
    movie_id: Annotated[int, Path(gt=0)],
    service: Annotated[IMovieService, Depends(get_movie_service)],
) -> MovieDetailResponse:
    movie = await service.get_movie(movie_id=movie_id)

    return MovieDetailResponse(**asdict(movie))


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
    response_model=ScreeningDetailResponse,
)
async def get_screenings_for_movie(
    movie_id: Annotated[int, Path(gt=0)],
    service: Annotated[IMovieService, Depends(get_movie_service)],
    date: Annotated[date | None, Query()] = None,
) -> ScreeningDetailResponse:
    screenings = await service.get_screenings_for_movie(movie_id=movie_id, date=date)
    return ScreeningDetailResponse(**asdict(screenings))
