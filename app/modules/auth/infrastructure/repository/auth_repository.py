from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.infrastructure.interface import IAuthRepository


class AuthRepository(IAuthRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def register_user(self, user) -> None:
        pass
