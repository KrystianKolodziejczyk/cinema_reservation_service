from datetime import date

from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cinema.application.dto import ScreeningDetailsDTO
from app.modules.cinema.domain.entities import Movie
from app.modules.cinema.infrastructure.interface import IMovieRepository
from app.modules.cinema.infrastructure.mappers import MovieMapper
from app.modules.cinema.infrastructure.orm import MovieORM


class MovieRepository(IMovieRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_movies(
        self, genre: str | None = None, title: str | None = None
    ) -> list[Movie]:
        stmt = select(MovieORM)
        if genre:
            stmt = stmt.where(MovieORM.genre == genre)
        if title:
            stmt = stmt.where(MovieORM.title.ilike(f"%{title}%"))

        result = await self._session.scalars(stmt)

        return [MovieMapper.to_entity(movie_orm) for movie_orm in result]

    async def fetch_movie(self, movie_id: int) -> Movie | None:
        stmt = select(MovieORM).where(MovieORM.movie_id == movie_id)
        movie_orm = await self._session.scalar(stmt)

        if not movie_orm:
            return

        return MovieMapper.to_entity(movie_orm=movie_orm)

    async def create_movie(self, movie: Movie) -> None:
        movie_orm = MovieMapper.to_orm(movie)
        self._session.add(movie_orm)
        await self._session.flush()

    async def delete_movie(self, movie_id: int) -> bool:
        stmt = (
            delete(MovieORM)
            .where(MovieORM.movie_id == movie_id)
            .returning(MovieORM.movie_id)
        )

        return bool(await self._session.scalar(stmt))

    async def fetch_screening_for_movie(
        self, movie_id: int, date: date | None
    ) -> list[ScreeningDetailsDTO] | None:
        stmt = text("""
            SELECT
                screenings.screening_id, 
                screenings.starts_at,
                halls.hall_name,
                halls.rows * halls.seats_per_row AS total_seats,
                screenings.price_normal,
                screenings.price_vip, 
                    ( 
                    SELECT COUNT(seats.seat_id)
                    FROM seats
                    WHERE seats.hall_id = halls.hall_id
                    AND seats.seat_id NOT IN (
                        SELECT rs.seat_id
                        FROM reserved_seats rs
                        JOIN reservations r ON rs.reservation_id = r.reservation_id
                        WHERE r.screening_id = screenings.screening_id
                        AND r.status NOT IN ('cancelled', 'expired')
                    )
                ) AS available_seats
            FROM screenings
            JOIN halls ON screenings.hall_id = halls.hall_id
            WHERE screenings.movie_id = :movie_id
            """)

        """
        if date:  # TODO: dodaj obsługe date
            stmt.where(
                ScreeningORM.starts_at >= date,
                ScreeningORM.starts_at < date + timedelta(days=1),
            )
        """
        result = (await self._session.execute(stmt)).all()

        if not result:
            return None

        return [
            ScreeningDetailsDTO(
                screening_id=screening_details.screening_id,
                starts_at=screening_details.starts_at,
                hall_name=screening_details.hall_name,
                available_seats=screening_details.available_seats,
                total_seats=screening_details.total_seats,
                price_normal=screening_details.price_normal,
                price_vip=screening_details.prive_vip,
            )
            for screening_details in result
        ]
