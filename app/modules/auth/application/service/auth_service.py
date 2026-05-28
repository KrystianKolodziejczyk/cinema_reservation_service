from datetime import datetime, timedelta

import jwt

from app.modules.auth.application.dto import RegisterUserDTO
from app.modules.auth.application.interface import IAuthService
from app.modules.auth.domain.entities.refresh_token import RefreshToken
from app.modules.auth.domain.entities.user import User
from app.modules.auth.infrastructure.interface import IAuthRepository


class AuthService(IAuthService):
    def __init__(self, repository: IAuthRepository) -> None:
        self._repository = repository

    def _create_access_token(self, user_id: int, role: str) -> str:
        payload = {
            "sub": str(user_id),
            "role": role,
            "iat": datetime.now().timestamp(),
            "exp": datetime.now().timestamp() + timedelta(minutes=15),
        }
        return jwt.encode(payload=payload, key="example_secret_key", algorithm="HS256")

    def _create_refresh_token(self, user_id: int) -> tuple[str | datetime, ...]:
        payload = {
            "sub": str(user_id),
            "iat": datetime.now().timestamp(),
            "exp": datetime.now().timestamp() + timedelta(days=7),
        }
        return jwt.encode(
            payload=payload, key="example_secret_key", algorithm="HS256"
        ), payload["exp"]

    async def register_user(self, dto: RegisterUserDTO) -> None:
        user = User(
            user_id=None,
            email=dto.email,
            password=dto.password,
            first_name=dto.first_name,
            last_name=dto.last_name,
        )
        if not user.compare_passwords(password_repeat=dto.password_repeat):
            pass  # TODO: dodaj raise

        user.hash_password()
        user_id = await self._repository.save_user(user=user)

        access_token = self._create_access_token(user_id=user_id, role="client")
        refresh_token, exp = self._create_refresh_token(user_id)

        refresh_token = RefreshToken(
            refresh_token_id=None,
            user_id=user_id,
            token_hash=refresh_token,
            expires_at=exp,
        )

        await self._repository.save_refresh_token(refresh_token)

        return {"access_token": access_token, "refresh_token": refresh_token}


# zrozum później jak powinna wyglądać autoryzajca
# + dowiedz się co zrobić żeby JWT był zawsze taki sam do Bruno
