from pydantic import BaseModel


class CreateReservationRequest(BaseModel):
    hold_id: int
    screening_id: int
