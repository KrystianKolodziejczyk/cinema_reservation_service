from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.application.interface import IHallService
from app.modules.cinema.application.service import HallService
from app.modules.cinema.infrastructure.repository import HallRepository
from app.modules.shared.database_conn.database_client import get_session


def get_hall_service(session: AsyncSession = Depends(get_session)) -> IHallService:
    return HallService(repository=HallRepository(session=session))
