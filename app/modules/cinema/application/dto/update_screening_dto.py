from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UpdateScreeningDTO:
    movie_id: int | None = None
    hall_id: int | None = None
    starts_at: datetime | None = None
    price_normal: int | None = None
    price_vip: int | None = None
