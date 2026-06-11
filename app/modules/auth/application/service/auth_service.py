import hashlib
from datetime import datetime, timedelta

import jwt
from sqlalchemy.exc import IntegrityError

from app.modules.auth.application.dto import LoginDTO, RegisterUserDTO
from app.modules.auth.application.exceptions import (
    DifferentPasswordsError,
    DuplicateEmailError,
    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    WrongPasswordError,
)
from app.modules.auth.application.interface import IAuthService
from app.modules.auth.domain.entities import RefreshToken, User
from app.modules.auth.infrastructure.interface import IAuthRepository
from app.modules.shared.config import settings
from app.modules.shared.exceptions import InvalidTokenError


class AuthService(IAuthService):
    def __init__(self, repository: IAuthRepository) -> None:
        self._repository = repository

    def _create_access_token(self, user_id: int, role: str) -> str:
        payload = {
            "sub": str(user_id),
            "iat": datetime.now().timestamp(),
            "exp": (datetime.now() + timedelta(minutes=15)).timestamp(),
            "role": role,
        }
        return jwt.encode(payload=payload, key=settings.secret_key, algorithm="HS256")

    def _create_refresh_token(self, user_id: int, role: str) -> tuple[str, datetime]:
        exp_dt = datetime.now() + timedelta(days=7)
        payload = {
            "sub": str(user_id),
            "iat": datetime.now().timestamp(),
            "exp": exp_dt.timestamp(),
            "role": role,
        }
        token = jwt.encode(payload=payload, key=settings.secret_key, algorithm="HS256")
        return token, exp_dt

    def _hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    async def _validate_refresh_token(self, token: str) -> tuple[RefreshToken, int, str]:
        try:
            payload = jwt.decode(token, key=settings.secret_key, algorithms=["HS256"])
            user_id = int(payload["sub"])
            role = payload["role"]
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError(status_code=409, detail="Invalid token") from e

        refresh_token = await self._repository.fetch_refresh_token(
            user_id=user_id, token=self._hash_token(token)
        )

        if not refresh_token:
            raise RefreshTokenNotFoundError(
                status_code=404, detail="Refresh token does not exist"
            )

        if refresh_token.expires_at < datetime.now():
            raise RefreshTokenExpiredError(
                status_code=409, detail="Refresh token expired"
            )

        return refresh_token, user_id, role

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

        try:
            user_id = await self._repository.save_user(user=user)
        except IntegrityError as e:
            raise DuplicateEmailError(
                status_code=409, detail="Email already in database"
            ) from e

        access_token = self._create_access_token(user_id=user_id, role=user._role)
        refresh_token_str, exp = self._create_refresh_token(user_id=user_id, role=user._role)

        refresh_token_entity = RefreshToken(
            refresh_token_id=None,
            user_id=user_id,
            token_hash=self._hash_token(refresh_token_str),
            expires_at=exp,
        )

        await self._repository.save_refresh_token(refresh_token_entity)

        return {"access_token": access_token, "refresh_token": refresh_token_str}

    async def login(self, dto: LoginDTO) -> dict[str, str]:
        user = await self._repository.fetch_user(email=dto.email)

        if not user.verify_password(raw_password=dto.password):
            raise WrongPasswordError(
                status_code=409, detail="Incorrect password entered"
            )

        access_token = self._create_access_token(user_id=user._user_id, role=user._role)
        refresh_token_str, exp = self._create_refresh_token(user_id=user._user_id, role=user._role)

        await self._repository.save_refresh_token(
            refresh_token=RefreshToken(
                refresh_token_id=None,
                user_id=user._user_id,
                token_hash=self._hash_token(refresh_token_str),
                expires_at=exp,
            )
        )

        return {"access_token": access_token, "refresh_token": refresh_token_str}

    async def logout(self, token: str) -> None:
        refresh_token, user_id, _ = await self._validate_refresh_token(token=token)

        await self._repository.delete_refresh_token(
            user_id=user_id, refresh_token_id=refresh_token.refresh_token_id
        )

    async def refresh(self, token: str) -> dict[str, str]:
        refresh_token, user_id, role = await self._validate_refresh_token(token=token)

        await self._repository.delete_refresh_token(
            user_id=user_id, refresh_token_id=refresh_token.refresh_token_id
        )

        access_token = self._create_access_token(user_id=user_id, role=role)
        new_refresh_token, exp = self._create_refresh_token(user_id=user_id, role=role)

        await self._repository.save_refresh_token(
            refresh_token=RefreshToken(
                refresh_token_id=None,
                user_id=user_id,
                token_hash=self._hash_token(new_refresh_token),
                expires_at=exp,
            )
        )

        return {"access_token": access_token, "refresh_token": new_refresh_token}
