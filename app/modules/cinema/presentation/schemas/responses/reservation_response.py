from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ReservationMovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    movie_id: int
    title: str
    poster_url: str | None


class ReservationHallResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    hall_id: int
    hall_name: str


class ReservationScreeningResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    screening_id: int | None
    starts_at: datetime
    ends_at: datetime
    status: str
    price_normal: int
    price_vip: int
    movie: ReservationMovieResponse
    hall: ReservationHallResponse


class ReservationSeatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    seat_id: int | None
    hall_id: int
    row: int
    number: int
    seat_type: Literal["normal", "vip"]


class ReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reservation_id: int | None
    user_id: int
    status: Literal["confirmed", "cancelled", "expired"]
    total_price: int
    created_at: datetime
    screening: ReservationScreeningResponse
    seats: list[ReservationSeatResponse]
