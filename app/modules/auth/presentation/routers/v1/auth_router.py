from fastapi import APIRouter, Depends

from app.modules.auth.application.dto import RegisterUserDTO
from app.modules.auth.application.service.auth_service import AuthService
from app.modules.auth.presentation.dependencies.auth_deps import get_auth_service
from app.modules.auth.presentation.schemas.requests import (
    RegisterUserRequest,
)

router = APIRouter(prefix="/v1/auth")


# ===============


@router.post("/register")
async def register_user(
    body: RegisterUserRequest, service: AuthService = Depends(get_auth_service)
):
    dto = RegisterUserDTO(**body.model_dump())
    service.register_user(dto=dto)
