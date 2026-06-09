from pydantic import BaseModel, Field


class HoldSeatsRequest(BaseModel):
    seat_ids: list[int] = Field(min_length=1)
