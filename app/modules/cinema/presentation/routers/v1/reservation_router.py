from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.modules.cinema.application.dto.create_reservation_dto import (
    CreateReservationDTO,
)
from app.modules.cinema.application.interface import IReservationService
from app.modules.cinema.presentation.dependencies import get_reservation_service
from app.modules.cinema.presentation.schemas.request import CreateReservationRequest
from app.modules.cinema.presentation.schemas.responses import (
    CreateReservationResponse,
    GetReservationResponse,
)
from app.modules.shared.dependencies.auth_deps import get_current_user

router = APIRouter(prefix="/v1/reservations")


# ==================


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreateReservationResponse
)
async def create_reservation(
    body: CreateReservationRequest,
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IReservationService, Depends(get_reservation_service)],
) -> CreateReservationResponse:
    dto = CreateReservationDTO(**body.model_dump())
    reservation_id = await service.create_reservation(
        user_id=user_data["user_id"], dto=dto
    )

    return CreateReservationResponse.model_validate({"reservation_id": reservation_id})


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


@router.put("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_reservation(
    reservation_id: Annotated[int, Path(gt=0)],
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IReservationService, Depends(get_reservation_service)],
) -> None:
    await service.cancel_reservation(reservation_id=reservation_id, user_data=user_data)
