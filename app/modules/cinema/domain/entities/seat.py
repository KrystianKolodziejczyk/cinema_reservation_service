from dataclasses import dataclass
from typing import Literal


@dataclass
class Seat:
    seat_id: int | None
    hall_id: int
    row: int
    number: int
    seat_type: Literal["normal", "vip"]
