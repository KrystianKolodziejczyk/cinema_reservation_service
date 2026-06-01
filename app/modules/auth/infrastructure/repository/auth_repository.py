from dataclasses import asdict

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.domain.entities import RefreshToken, User
from app.modules.auth.infrastructure.interface import IAuthRepository
from app.modules.auth.infrastructure.orm import RefreshTokenORM, UserORM


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

    async def fetch_user(self, email: str) -> User:
        stmt = select(UserORM).where(UserORM.email == email)
        user_orm = await self._session.scalar(stmt)
        return User(
            user_id=user_orm.user_id,
            email=user_orm.email,
            password=user_orm.password_hash,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
        )  # TODO: dodaj mappery

    async def delete_refresh_token(self, user_id: int, refresh_token_id: int) -> None:
        stmt = delete(RefreshTokenORM).where(
            RefreshTokenORM.user_id == user_id,
            RefreshTokenORM.refresh_token_id == refresh_token_id,
        )
        await self._session.execute(stmt)

    async def fetch_refresh_token(
        self, user_id: int, token: str
    ) -> RefreshToken | None:
        stmt = select(RefreshTokenORM).where(
            RefreshTokenORM.user_id == user_id, RefreshTokenORM.token_hash == token
        )
        refresh_token_orm = await self._session.scalar(stmt)

        if not refresh_token_orm:
            return None

        return RefreshToken(
            refresh_token_id=refresh_token_orm.refresh_token_id,
            user_id=refresh_token_orm.user_id,
            token_hash=refresh_token_orm.token_hash,
            expires_at=refresh_token_orm.expires_at,
        )
