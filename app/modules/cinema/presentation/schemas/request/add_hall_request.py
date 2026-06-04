from pydantic import BaseModel, Field


class AddHallRequest(BaseModel):
    hall_name: str = Field(min_length=2)
    rows: int = Field(gt=0, le=15)
    seats_per_row: int = Field(gt=0, le=20)
