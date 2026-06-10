from dataclasses import dataclass
from typing import Literal


@dataclass
class Reservation:
    reservation_id: int | None
    user_id: int
    screening_id: int
    status: Literal["pending", "confirmed", "cancelled", "expired"]
    total_price: int
    conf_code: str
