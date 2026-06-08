from datetime import datetime

from pydantic import BaseModel, Field


class UpdateScreeningRequest(BaseModel):
    movie_id: int | None = Field(default=None)
    hall_id: int | None = Field(default=None)
    starts_at: datetime | None = Field(default=None)
    price_normal: int | None = Field(default=None)
    price_vip: int | None = Field(default=None)
