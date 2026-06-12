from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.modules.cinema.application.dto.create_reservation_dto import (
    CreateReservationDTO,
)
from app.modules.cinema.application.interface import IReservationService
from app.modules.cinema.presentation.dependencies import get_reservation_service
from app.modules.cinema.presentation.schemas.request import CreateReservationRequest
from app.modules.cinema.presentation.schemas.responses import GetReservationResponse
from app.modules.shared.dependencies.auth_deps import get_current_user

router = APIRouter(prefix="/v1/reservations")


# ==================


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_reservation(
    body: CreateReservationRequest,
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IReservationService, Depends(get_reservation_service)],
) -> None:
    dto = CreateReservationDTO(**body.model_dump())
    await service.create_reservation(user_id=user_data["user_id"], dto=dto)


@router.get(
    "/{reservation_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetReservationResponse,
)
async def get_reservation(
    reservation_id: Annotated[int, Path(gt=0)],
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IReservationService, Depends(get_reservation_service)],
) -> GetReservationResponse:
    reservation_details = await service.get_reservation(
        reservation_id=reservation_id, user_data=user_data
    )

    return GetReservationResponse.model_validate(reservation_details)
