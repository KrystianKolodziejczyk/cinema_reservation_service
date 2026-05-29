from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.domain.entities.refresh_token import RefreshToken
from app.modules.auth.domain.entities.user import User
from app.modules.auth.infrastructure.interface import IAuthRepository
from app.modules.auth.infrastructure.orm import UserORM
from app.modules.auth.infrastructure.orm.refresh_token_orm import RefreshTokenORM


class AuthRepository(IAuthRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_user(self, user: User) -> int:
        user_orm = UserORM(
            user_id=None,
            email=user._email,
            password_hash=user._password,
            first_name=user._first_name,
            last_name=user._last_name,
        )
        self._session.add(user_orm)
        await self._session.flush()

        return user_orm.user_id

    async def save_refresh_token(self, refresh_token: RefreshToken) -> None:
        refresh_token_orm = RefreshTokenORM(**asdict(refresh_token))
        self._session.add(refresh_token_orm)
        await self._session.flush()

    async def fetch_password(self, email: str) -> User:
        stmt = select(UserORM).where(UserORM.email == email)
        user_orm = await self._session.scalar(stmt)
        return User(
            user_id=user_orm.user_id,
            email=user_orm.email,
            password=user_orm.password_hash,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
        )  # TODO: dodaj mappery
