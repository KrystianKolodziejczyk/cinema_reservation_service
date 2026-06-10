from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.application.interface import IReservationService
from app.modules.cinema.application.service import ReservationService
from app.modules.cinema.infrastructure.repository import (
    ReservationHoldRepository,
    ReservationRepository,
)
from app.modules.shared.database_conn.database_client import get_session
from app.modules.shared.database_conn.redis_client import redis_client


def get_reservation_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> IReservationService:
    return ReservationService(
        repository=ReservationRepository(session=session),
        redis_repository=ReservationHoldRepository(redis_client=redis_client),
    )
