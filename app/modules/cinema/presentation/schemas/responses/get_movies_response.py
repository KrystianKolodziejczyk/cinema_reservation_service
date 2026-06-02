from pydantic import BaseModel

from app.modules.cinema.presentation.schemas.responses.one_movie_response import (
    OneMovieResponse,
)


class GetMoviesResponse(BaseModel):
    items: list[OneMovieResponse]
