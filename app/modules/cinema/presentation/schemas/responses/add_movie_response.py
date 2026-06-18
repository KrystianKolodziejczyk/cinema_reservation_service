from pydantic import BaseModel


class AddMovieResponse(BaseModel):
    movie_id: int
