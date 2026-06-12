from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ReservationScreeningResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    screening_id: int | None
    movie_id: int
    hall_id: int
    starts_at: datetime
    price_normal: int
    price_vip: int
    status: str


class ReservationSeatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    seat_id: int | None
    hall_id: int
    row: int
    number: int
    seat_type: Literal["normal", "vip"]


class GetReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reservation_id: int | None
    user_id: int
    status: Literal["pending", "confirmed", "cancelled", "expired"]
    total_price: int
    conf_code: str
    screening: ReservationScreeningResponse
    seats: list[ReservationSeatResponse]
