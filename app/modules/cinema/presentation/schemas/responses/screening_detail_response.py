from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ScreeningMovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    movie_id: int
    title: str
    description: str
    director: str
    duration: int
    genre: str
    rating: float
    poster_url: str | None


class ScreeningSeatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    seat_id: int
    row: int
    number: int
    seat_type: str
    status: str
    price: int


class ScreeningDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    screening_id: int
    movie: ScreeningMovieResponse
    starts_at: datetime
    ends_at: datetime
    status: Literal["scheduled", "ongoing", "cancelled", "completed"]
    hall_name: str
    seats: list[ScreeningSeatResponse]
