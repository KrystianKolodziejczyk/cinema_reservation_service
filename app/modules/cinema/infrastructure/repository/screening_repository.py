from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.application.excpetions import ScreeningNotFoundError
from app.modules.cinema.domain.entities import Screening
from app.modules.cinema.infrastructure.interface import IScreeningRepository
from app.modules.cinema.infrastructure.mappers import ScreeningMapper
from app.modules.cinema.infrastructure.orm.screening_orm import ScreeningORM


class ScreeningRepository(IScreeningRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_screenings(self, screenings: list[Screening]) -> None:
        screenings_orm = [ScreeningMapper.to_orm(screening) for screening in screenings]

        self._session.add_all(screenings_orm)
        await self._session.flush()

    async def delete_screening(self, screening_id: int) -> bool:
        stmt = (
            delete(ScreeningORM)
            .where(ScreeningORM.screening_id == screening_id)
            .returning(ScreeningORM.screening_id)
        )

        return bool(await self._session.scalar(stmt))

    async def fetch_screening(self, screening_id: int) -> Screening:
        stmt = select(ScreeningORM).where(ScreeningORM.screening_id == screening_id)
        screening_orm = await self._session.scalar(stmt)

        if screening_orm is None:
            raise ScreeningNotFoundError(
                status_code=404, detail="Screening does not exist"
            )

        return ScreeningMapper.to_entity(screening_orm=screening_orm)

    async def save_screening(self, screening: Screening) -> None:
        screening_orm = ScreeningMapper.to_orm(screening)

        await self._session.merge(screening_orm)
        await self._session.flush()
