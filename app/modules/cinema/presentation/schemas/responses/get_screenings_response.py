from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class MovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    director: str
    duration: int
    genre: str
    rating: float


class SeatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    seat_id: int
    row: int
    number: int
    seat_type: str
    status: str
    price: int


class GetScreeningResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    screening_id: int
    movie: MovieResponse
    starts_at: datetime
    ends_at: datetime
    status: Literal["scheduled", "ongoing", "cancelled", "completed"]
    hall_name: str
    seats: list[SeatResponse]
