from datetime import datetime

from pydantic import BaseModel


class OneScreeningResponse(BaseModel):
    screening_id: int | None
    movie_id: int
    hall_id: int
    starts_at: datetime
    price_normal: int
    price_vip: int
    status: str
