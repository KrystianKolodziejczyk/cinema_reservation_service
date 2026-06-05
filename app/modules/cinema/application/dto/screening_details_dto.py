from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ScreeningDetailsDTO:
    screening_id: int
    starts_at: datetime
    hall_name: str
    available_seats: int
    total_seats: int
    price_normal: int
    price_vip: int
