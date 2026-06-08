from __future__ import annotations

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

    def update_fields(self, **kwargs) -> Screening:
        for field, value in kwargs.items():
            if value is not None:
                setattr(self, field, value)

        return self
