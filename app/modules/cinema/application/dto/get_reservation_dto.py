from dataclasses import dataclass
from typing import Literal

from app.modules.cinema.domain.entities import Screening, Seat


@dataclass(frozen=True)
class GetReservationDTO:
    reservation_id: int | None
    user_id: int
    status: Literal["pending", "confirmed", "cancelled", "expired"]
    total_price: int
    screening: Screening
    seats: list[Seat]
