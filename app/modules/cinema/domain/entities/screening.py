from dataclasses import dataclass
from datetime import datetime


@dataclass
class Screening:
    screening_id: int | None
    movie_id: int
    hall_id: int
    starts_at: datetime
    price_normal: int
    price_vip: int
    status: str
