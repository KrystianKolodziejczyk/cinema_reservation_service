from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.modules.cinema.application.dto import AddScreeningDTO
from app.modules.cinema.application.interface import IScreeningService
from app.modules.cinema.presentation.dependencies import get_screening_service
from app.modules.cinema.presentation.schemas.request import (
    AddScreeningRequest,
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
