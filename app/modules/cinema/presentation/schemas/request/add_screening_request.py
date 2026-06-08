from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class AddScreeningRequest(BaseModel):
    movie_id: int
    hall_id: int
    starts_at: list[datetime]
    price_normal: int
    price_vip: int
    status: Literal["scheduled", "ongoing", "completed", "canceled"] = Field(
        default="scheduled"
    )
