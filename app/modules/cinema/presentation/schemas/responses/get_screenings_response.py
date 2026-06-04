from pydantic import BaseModel

from app.modules.cinema.presentation.schemas.responses.one_screening_response import (
    OneScreeningResponse,
)


class GetScreeningResponse(BaseModel):
    screenings: list[OneScreeningResponse]
