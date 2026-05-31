from fastapi import APIRouter, Depends, status

from app.modules.auth.application.dto import RegisterUserDTO
from app.modules.auth.application.dto.login_dto import LoginDTO
from app.modules.auth.application.interface.i_auth_service import IAuthService
from app.modules.auth.presentation.dependencies.auth_deps import get_auth_service
from app.modules.auth.presentation.schemas.requests import (
    RegisterUserRequest,
)
from app.modules.auth.presentation.schemas.requests.login_request import LoginRequest
from app.modules.auth.presentation.schemas.responses import (
    RegisterUserResponse,
)
from app.modules.auth.presentation.schemas.responses.login_response import LoginResponse
from app.modules.shared.dependencies.auth_deps import get_current_user

router = APIRouter(prefix="/v1/auth")


# ===============


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterUserResponse,
)
async def register_user(
    body: RegisterUserRequest, service: IAuthService = Depends(get_auth_service)
) -> RegisterUserResponse:
    dto = RegisterUserDTO(**body.model_dump())
    tokens = await service.register_user(dto=dto)
    return RegisterUserResponse(**tokens)


@router.post(
    "/login", status_code=status.HTTP_201_CREATED, response_model=LoginResponse
)
async def login(
    body: LoginRequest, service: IAuthService = Depends(get_auth_service)
) -> LoginResponse:
    dto = LoginDTO(**body.model_dump())
    tokens = await service.login(dto=dto)
    return LoginResponse(**tokens)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    service: IAuthService = Depends(get_auth_service),
    user_id: int = Depends(get_current_user),
) -> None:
    await service.logout(user_id)
