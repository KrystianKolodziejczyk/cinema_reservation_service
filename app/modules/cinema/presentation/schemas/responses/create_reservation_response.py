from pydantic import BaseModel


class CreateReservationResponse(BaseModel):
    reservation_id: int
