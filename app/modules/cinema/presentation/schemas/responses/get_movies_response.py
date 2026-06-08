from app.modules.cinema.presentation.schemas.responses.one_movie_response import (
    OneMovieResponse,
)
from pydantic import BaseModel


class GetMoviesResponse(BaseModel):
    items: list[OneMovieResponse]
