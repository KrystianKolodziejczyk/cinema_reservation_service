from dataclasses import dataclass
from typing import Literal


@dataclass
class ScreeningSeat:
    screening_id: int
    seat_id: int
    status: Literal["free", "reserved", "cancelled"]
