from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.modules.cinema.application.dto import AddHallDTO
from app.modules.cinema.application.interface.i_hall_service import IHallService
from app.modules.cinema.presentation.dependencies import get_hall_service
from app.modules.cinema.presentation.schemas.request import AddHallRequest
from app.modules.shared.dependencies.auth_deps import get_current_user

router = APIRouter(prefix="/v1/halls")


# ==================


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_hall(
    body: AddHallRequest,
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IHallService, Depends(get_hall_service)],
) -> None:
    dto = AddHallDTO(**body.model_dump())
    await service.add_hall(dto=dto, user_role=user_data["role"])


@router.delete("/{hall_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hall(
    hall_id: int,
    user_data: Annotated[dict, Depends(get_current_user)],
    service: Annotated[IHallService, Depends(get_hall_service)],
) -> None:
    await service.delete_hall(hall_id=hall_id, user_role=user_data["role"])
