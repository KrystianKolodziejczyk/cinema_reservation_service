from pydantic import BaseModel


class AddHallResponse(BaseModel):
    hall_id: int
