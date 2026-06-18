from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.cinema.application.dto import (
    MovieData,
    ScreeningDetailsDTO,
    SeatData,
    SeatHoldData,
)
from app.modules.cinema.application.excpetions import ScreeningNotFoundError
from app.modules.cinema.domain.entities import Screening
from app.modules.cinema.infrastructure.interface import IScreeningRepository
from app.modules.cinema.infrastructure.mappers import ScreeningMapper
from app.modules.cinema.infrastructure.orm import (
    HallORM,
    ReservationORM,
    ScreeningORM,
    ScreeningSeatORM,
    SeatORM,
)


class ScreeningRepository(IScreeningRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_screenings(self, screenings: list[Screening]) -> list[int]:
        screenings_orm = [ScreeningMapper.to_orm(screening) for screening in screenings]

        self._session.add_all(screenings_orm)
        await self._session.flush()

        return [s.screening_id for s in screenings_orm]

    async def delete_screening(self, screening_id: int) -> bool:
        stmt = (
            delete(ScreeningORM)
            .where(ScreeningORM.screening_id == screening_id)
            .returning(ScreeningORM.screening_id)
        )

        return bool(await self._session.scalar(stmt))

    async def fetch_basic_screening(self, screening_id: int) -> Screening:
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

    async def fetch_screening_with_relations(
        self, screening_id: int
    ) -> ScreeningDetailsDTO | None:
        stmt = (
            select(ScreeningORM)
            .where(ScreeningORM.screening_id == screening_id)
            .options(
                selectinload(ScreeningORM.movie),
                selectinload(ScreeningORM.hall),
                selectinload(ScreeningORM.screening_seats).selectinload(
                    ScreeningSeatORM.seat
                ),
            )
        )

        screening_orm = await self._session.scalar(stmt)

        if not screening_orm:
            return None

        return ScreeningDetailsDTO(
            screening_id=screening_orm.screening_id,
            movie=MovieData(
                movie_id=screening_orm.movie.movie_id,
                title=screening_orm.movie.title,
                description=screening_orm.movie.description,
                director=screening_orm.movie.director,
                duration=screening_orm.movie.duration,
                genre=screening_orm.movie.genre,
                rating=screening_orm.movie.rating,
                poster_url=screening_orm.movie.poster_url,
            ),
            starts_at=screening_orm.starts_at,
            ends_at=screening_orm.ends_at,
            status=screening_orm.status,
            hall_name=screening_orm.hall.hall_name,
            seats=[
                SeatData(
                    seat_id=ss.seat.seat_id,
                    row=ss.seat.row,
                    number=ss.seat.number,
                    seat_type=ss.seat.seat_type,
                    status=ss.status,
                    price=screening_orm.price_normal
                    if ss.seat.seat_type == "normal"
                    else screening_orm.price_vip,
                )
                for ss in screening_orm.screening_seats
            ],
        )

    async def fetch_seats_by_ids(
        self, screening_id: int, seat_ids: list[int]
    ) -> list[SeatHoldData]:
        stmt = (
            select(
                SeatORM.seat_id,
                SeatORM.row,
                SeatORM.number,
                SeatORM.seat_type,
                ScreeningORM.price_normal,
                ScreeningORM.price_vip,
            )
            .join(HallORM, SeatORM.hall_id == HallORM.hall_id)
            .join(ScreeningORM, ScreeningORM.hall_id == HallORM.hall_id)
            .where(
                ScreeningORM.screening_id == screening_id,
                SeatORM.seat_id.in_(seat_ids),
            )
        )

        rows = (await self._session.execute(stmt)).all()

        return [
            SeatHoldData(
                seat_id=row.seat_id,
                row=row.row,
                number=row.number,
                price=row.price_normal if row.seat_type == "normal" else row.price_vip,
                seat_type=row.seat_type,
            )
            for row in rows
        ]

    async def get_screening_for_reservation(
        self, reservation_id: int, user_id: int
    ) -> Screening:
        subq = (
            select(ReservationORM.screening_id)
            .where(
                ReservationORM.reservation_id == reservation_id,
                ReservationORM.user_id == user_id,
            )
            .scalar_subquery()
        )

        stmt = select(ScreeningORM).where(ScreeningORM.screening_id == subq)

        screening_orm = await self._session.scalar(stmt)

        return ScreeningMapper.to_entity(screening_orm)
