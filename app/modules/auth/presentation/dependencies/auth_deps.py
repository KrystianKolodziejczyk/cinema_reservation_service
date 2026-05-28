from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.application.interface import IAuthService
from app.modules.auth.application.service import AuthService
from app.modules.auth.infrastructure.repository.auth_repository import AuthRepository
from app.modules.shared.database_conn.database_client import get_session


def get_auth_service(session: AsyncSession = Depends(get_session)) -> IAuthService:  # noqa
    return AuthService(repository=AuthRepository(session=session))
