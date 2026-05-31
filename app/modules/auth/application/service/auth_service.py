from datetime import datetime, timedelta

import jwt

from app.modules.auth.application.dto import RegisterUserDTO
from app.modules.auth.application.dto.login_dto import LoginDTO
from app.modules.auth.application.exceptions import DifferentPasswordsError
from app.modules.auth.application.exceptions.refresh_token_not_found_error import (
    RefreshTokenNotFoundError,
)
from app.modules.auth.application.exceptions.wrong_password_error import (
    WrongPasswordError,
)
from app.modules.auth.application.interface import IAuthService
from app.modules.auth.domain.entities.refresh_token import RefreshToken
from app.modules.auth.domain.entities.user import User
from app.modules.auth.infrastructure.interface import IAuthRepository
from app.modules.shared.config.settings import settings


class AuthService(IAuthService):
    def __init__(self, repository: IAuthRepository) -> None:
        self._repository = repository

    def _create_access_token(self, user_id: int, role: str) -> str:
        payload = {
            "sub": str(user_id),
            "role": role,
            "iat": datetime.now().timestamp(),
            "exp": (datetime.now() + timedelta(minutes=15)).timestamp(),
        }
        return jwt.encode(payload=payload, key=settings.secret_key, algorithm="HS256")

    def _create_refresh_token(self, user_id: int) -> tuple[str, datetime]:
        exp_dt = datetime.now() + timedelta(days=7)
        payload = {
            "sub": str(user_id),
            "iat": datetime.now().timestamp(),
            "exp": exp_dt.timestamp(),
        }
        token = jwt.encode(payload=payload, key=settings.secret_key, algorithm="HS256")
        return token, exp_dt

    async def register_user(self, dto: RegisterUserDTO) -> dict[str, str]:
        user = User(
            user_id=None,
            email=dto.email,
            password=dto.password,
            first_name=dto.first_name,
            last_name=dto.last_name,
        )
        if not user.compare_passwords(password_repeat=dto.password_repeat):
            raise DifferentPasswordsError(
                status_code=409, detail="Two different passwords were entered"
            )

        user.hash_password()
        user_id = await self._repository.save_user(user=user)

        access_token = self._create_access_token(user_id=user_id, role="client")
        refresh_token_str, exp = self._create_refresh_token(user_id)

        refresh_token_entity = RefreshToken(
            refresh_token_id=None,
            user_id=user_id,
            token_hash=refresh_token_str,
            expires_at=exp,
        )

        await self._repository.save_refresh_token(refresh_token_entity)

        return {"access_token": access_token, "refresh_token": refresh_token_str}

    async def login(self, dto: LoginDTO) -> dict[str, str]:
        user = await self._repository.fetch_password(email=dto.email)

        if not user.verify_password(raw_password=dto.password):
            raise WrongPasswordError(
                status_code=409, detail="Incorrect password entered"
            )

        access_token = self._create_access_token(user_id=user._user_id, role="client")
        refresh_token_str, exp = self._create_refresh_token(user_id=user._user_id)

        await self._repository.save_refresh_token(
            refresh_token=RefreshToken(
                refresh_token_id=None,
                user_id=user._user_id,
                token_hash=refresh_token_str,
                expires_at=exp,
            )
        )

        return {"access_token": access_token, "refresh_token": refresh_token_str}

    async def logout(self, user_id: int) -> None:
        await self._repository.delete_refresh_token(user_id=user_id)

    async def refresh(self, user_id: int, token: str) -> dict[str, str]:
        result = await self._repository.fetch_refresh_token_id(
            user_id=user_id, token=token
        )
        if not result:
            raise RefreshTokenNotFoundError(
                status_code=404, detail="Refresh token does not exist"
            )
        await self._repository.delete_refresh_token(user_id=user_id)

        access_token = self._create_access_token(user_id=user_id, role="client")
        refresh_token, exp = self._create_refresh_token(user_id=user_id)

        await self._repository.save_refresh_token(
            refresh_token=RefreshToken(
                refresh_token_id=None,
                user_id=user_id,
                token_hash=refresh_token,
                expires_at=exp,
            )
        )

        return {"access_token": access_token, "refresh_token": refresh_token}
