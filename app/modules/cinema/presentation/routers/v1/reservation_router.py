from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.modules.cinema.application.dto import (
    CreateReservationDTO,
)
from app.modules.cinema.application.interface import IReservationService
from app.modules.cinema.presentation.dependencies import get_reservation_service
from app.modules.cinema.presentation.schemas.request import CreateReservationRequest
from app.modules.cinema.presentation.schemas.responses import (
    ReservationHistoryResponse,
    ReservationResponse,
)
from app.modules.shared.dependencies.auth_deps import get_current_user

router = APIRouter(prefix="/v1/reservations")


# ==================


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=ReservationResponse
)
async def create_reservation(
    body: CreateReservationRequest,
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IReservationService, Depends(get_reservation_service)],
) -> ReservationResponse:
    dto = CreateReservationDTO(**body.model_dump())
    reservation = await service.create_reservation(
        user_id=user_data["user_id"], dto=dto
    )
    return ReservationResponse.model_validate(reservation)


@router.get(
    "/me", status_code=status.HTTP_200_OK, response_model=ReservationHistoryResponse
)
async def get_reservation_history(
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IReservationService, Depends(get_reservation_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> ReservationHistoryResponse:
    reservations, total = await service.get_reservation_history(
        user_id=user_data["user_id"], page=page, limit=limit
    )
    return ReservationHistoryResponse.model_validate(
        {"reservations": reservations, "total": total, "page": page, "limit": limit}
    )


@router.get(
    "/{reservation_id}",
    status_code=status.HTTP_200_OK,
    response_model=ReservationResponse,
)
async def get_reservation(
    reservation_id: Annotated[int, Path(gt=0)],
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IReservationService, Depends(get_reservation_service)],
) -> ReservationResponse:
    reservation_details = await service.get_reservation(
        reservation_id=reservation_id, user_data=user_data
    )

    return ReservationResponse.model_validate(reservation_details)


@router.put("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_reservation(
    reservation_id: Annotated[int, Path(gt=0)],
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IReservationService, Depends(get_reservation_service)],
) -> None:
    await service.cancel_reservation(reservation_id=reservation_id, user_data=user_data)
