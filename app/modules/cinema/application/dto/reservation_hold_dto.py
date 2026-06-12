from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SeatHoldData:
    seat_id: int
    row: int
    number: int
    price: int


@dataclass(frozen=True)
class ReservationHoldDTO:
    hold_id: int
    expires_at: datetime
    seats: list[SeatHoldData]
    total_price: int


@dataclass(frozen=True)
class HoldDTO:
    hold_id: int
    user_id: int
    screening_id: int
    seat_ids: list[int]
    seats: list[SeatHoldData]
    total_price: int
    expires_at: datetime
