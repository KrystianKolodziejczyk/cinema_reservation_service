from dataclasses import dataclass
from typing import Literal


@dataclass
class ScreeningSeat:
    screening_id: int
    seat_id: int
    reservation_id: int | None
    status: Literal["free", "reserved", "cancelled"]
