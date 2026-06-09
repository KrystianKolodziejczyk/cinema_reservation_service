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
