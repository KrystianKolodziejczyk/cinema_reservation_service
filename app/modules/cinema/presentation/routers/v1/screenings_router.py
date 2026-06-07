from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.modules.cinema.application.dto import AddScreeningDTO, UpdateScreeningDTO
from app.modules.cinema.application.interface import IScreeningService
from app.modules.cinema.presentation.dependencies import get_screening_service
from app.modules.cinema.presentation.schemas.request import (
    AddScreeningRequest,
    UpdateScreeningRequest,
)
from app.modules.cinema.presentation.schemas.responses.get_screenings_response import (
    GetScreeningResponse,
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
