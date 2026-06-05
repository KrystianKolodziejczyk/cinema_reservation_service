from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass(frozen=True)
class AddScreeningDTO:
    movie_id: int
    hall_id: int
    starts_at: list[datetime]
    price_normal: int
    price_vip: int
    status: Literal["scheduled", "ongoing", "completed", "canceled"] = "scheduled"
