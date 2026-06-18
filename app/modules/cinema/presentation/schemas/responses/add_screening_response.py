from pydantic import BaseModel


class AddScreeningResponse(BaseModel):
    screening_ids: list[int]
