from pydantic import BaseModel

from app.modules.cinema.presentation.schemas.responses.get_reservation_respone import (
    GetReservationResponse,
)


class GetReservationHisotryResponse(BaseModel):
    reservations: list[GetReservationResponse]
