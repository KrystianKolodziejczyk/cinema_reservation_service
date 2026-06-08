from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.application.interface import IScreeningService
from app.modules.cinema.application.service import ScreeningService
from app.modules.cinema.infrastructure.repository import ScreeningRepository
from app.modules.shared.database_conn.database_client import get_session


def get_screening_service(
    session: AsyncSession = Depends(get_session),
) -> IScreeningService:
    return ScreeningService(repository=ScreeningRepository(session=session))
