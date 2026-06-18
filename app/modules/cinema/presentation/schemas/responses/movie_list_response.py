from pydantic import BaseModel

from app.modules.cinema.presentation.schemas.responses.movie_detail_response import (
    MovieDetailResponse,
)


class MovieListResponse(BaseModel):
    items: list[MovieDetailResponse]
    total: int
    page: int
    limit: int
