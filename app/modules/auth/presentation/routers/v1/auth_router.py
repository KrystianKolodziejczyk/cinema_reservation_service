from fastapi import APIRouter, Depends, status

from app.modules.auth.application.dto import RegisterUserDTO
from app.modules.auth.application.service.auth_service import AuthService
from app.modules.auth.presentation.dependencies.auth_deps import get_auth_service
from app.modules.auth.presentation.schemas.requests import (
    RegisterUserRequest,
)
from app.modules.auth.presentation.schemas.responses import (
    RegisterUserResponse,
)

router = APIRouter(prefix="/v1/auth")


# ===============


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterUserResponse,
)
async def register_user(
    body: RegisterUserRequest, service: AuthService = Depends(get_auth_service)
) -> RegisterUserResponse:
    dto = RegisterUserDTO(**body.model_dump())
    tokens = await service.register_user(dto=dto)
    return RegisterUserResponse(**tokens)
