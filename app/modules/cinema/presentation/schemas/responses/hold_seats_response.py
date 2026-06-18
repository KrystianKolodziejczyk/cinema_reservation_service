from datetime import datetime

from pydantic import BaseModel


class SeatHoldResponse(BaseModel):
    seat_id: int
    row: int
    number: int
    price: int
    seat_type: str


class HoldSeatsResponse(BaseModel):
    hold_id: int
    expires_at: datetime
    seats: list[SeatHoldResponse]
    total_price: int

    model_config = {"from_attributes": True}
