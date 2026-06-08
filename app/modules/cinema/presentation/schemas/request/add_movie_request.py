from pydantic import BaseModel, Field


class AddMovieRequest(BaseModel):
    title: str = Field(min_length=2)
    description: str = Field(min_length=2)
    director: str = Field(min_length=2)
    duration: int = Field(gt=0)
    genre: str = Field(min_length=2)
    rating: float = Field(gt=0.0, le=5.0)
    poster_url: str | None = Field(default=None)
