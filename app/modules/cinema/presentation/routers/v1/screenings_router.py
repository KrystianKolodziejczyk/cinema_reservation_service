from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.modules.cinema.application.dto import AddScreeningDTO, UpdateScreeningDTO
from app.modules.cinema.application.interface import IScreeningService
from app.modules.cinema.presentation.dependencies import get_screening_service
from app.modules.cinema.presentation.schemas.request import (
    AddScreeningRequest,
    HoldSeatsRequest,
    UpdateScreeningRequest,
)
from app.modules.cinema.presentation.schemas.responses import (
    GetScreeningResponse,
    HoldSeatsResponse,
)
from app.modules.shared.dependencies.auth_deps import get_current_user

router = APIRouter(prefix="/v1/screenings")

# ===============


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_screening(
    body: AddScreeningRequest,
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IScreeningService, Depends(get_screening_service)],
) -> None:
    dto = AddScreeningDTO(**body.model_dump())
    await service.add_screening(dto=dto, user_role=user_data["role"])


@router.delete("/{screening_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_screening(
    screening_id: int,
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IScreeningService, Depends(get_screening_service)],
) -> None:
    await service.delete_screening(
        screening_id=screening_id, user_role=user_data["role"]
    )


@router.put("/{screening_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_screening(
    screening_id: int,
    body: UpdateScreeningRequest,
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IScreeningService, Depends(get_screening_service)],
) -> None:
    dto = UpdateScreeningDTO(**body.model_dump())
    await service.update_screening(
        screening_id=screening_id, dto=dto, user_role=user_data["role"]
    )


@router.get(
    "/{screening_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetScreeningResponse,
)
async def get_screening(
    screening_id: int,
    service: Annotated[IScreeningService, Depends(get_screening_service)],
) -> GetScreeningResponse:
    screening_details = await service.get_screening(screening_id=screening_id)
    return GetScreeningResponse.model_validate(screening_details)


@router.post(
    "/{screening_id}/seats/hold",
    status_code=status.HTTP_200_OK,
    response_model=HoldSeatsResponse,
)
async def hold_seats(
    screening_id: int,
    body: HoldSeatsRequest,
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IScreeningService, Depends(get_screening_service)],
) -> HoldSeatsResponse:
    result = await service.hold_seats(
        seat_ids=body.seat_ids,
        user_id=user_data["user_id"],
        screening_id=screening_id,
    )
    return HoldSeatsResponse.model_validate(result, from_attributes=True)


@router.delete(
    "/{screening_id}/seats/hold/{hold_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def release_hold(
    screening_id: int,
    hold_id: int,
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IScreeningService, Depends(get_screening_service)],
) -> None:
    await service.release_hold(
        hold_id=hold_id,
        user_id=user_data["user_id"],
        screening_id=screening_id,
    )
