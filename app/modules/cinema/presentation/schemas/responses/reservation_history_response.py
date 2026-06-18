from pydantic import BaseModel

from app.modules.cinema.presentation.schemas.responses.reservation_response import (
    ReservationResponse,
)


class ReservationHistoryResponse(BaseModel):
    reservations: list[ReservationResponse]
    total: int
    page: int
    limit: int
