from pydantic import BaseModel, ConfigDict


class MovieDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    movie_id: int
    title: str
    description: str
    director: str
    duration: int
    genre: str
    rating: float
    poster_url: str | None
