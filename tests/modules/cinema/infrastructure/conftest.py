from datetime import datetime, timedelta

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.domain.entities import User
from app.modules.auth.infrastructure.repository import AuthRepository
from app.modules.cinema.domain.entities import Hall, Movie, Screening, ScreeningSeat, Seat
from app.modules.cinema.infrastructure.interface import (
    IHallRepository,
    IMovieRepository,
    IReservationRepository,
    IScreeningRepository,
    IScreeningSeatRepository,
)
from app.modules.cinema.infrastructure.repository import (
    HallRepository,
    MovieRepository,
    ReservationRepository,
    ScreeningRepository,
    ScreeningSeatRepository,
)


@pytest.fixture
def movie_repository(db_session: AsyncSession) -> IMovieRepository:
    return MovieRepository(session=db_session)


@pytest.fixture
def hall_repository(db_session: AsyncSession) -> IHallRepository:
    return HallRepository(session=db_session)


@pytest.fixture
def screening_repository(db_session: AsyncSession) -> IScreeningRepository:
    return ScreeningRepository(session=db_session)


@pytest.fixture
def screening_seat_repository(db_session: AsyncSession) -> IScreeningSeatRepository:
    return ScreeningSeatRepository(session=db_session)


@pytest.fixture
async def db_movie(movie_repository: IMovieRepository) -> Movie:
    movie = Movie(
        movie_id=None,
        title="Fixture Movie",
        description="Used as FK dependency",
        director="Director",
        duration=100,
        genre="drama",
        rating=4.0,
        poster_url=None,
    )
    movie_id = await movie_repository.create_movie(movie=movie)
    return Movie(movie_id=movie_id, **{k: v for k, v in movie.__dict__.items() if k != "movie_id"})


@pytest.fixture
async def db_hall(hall_repository: IHallRepository) -> Hall:
    hall = Hall(hall_id=None, hall_name="Fixture Hall", rows=3, seats_per_row=4)
    hall_id = await hall_repository.create_hall(hall=hall)
    seats = [
        Seat(seat_id=None, hall_id=hall_id, row=r, number=n, seat_type="normal")
        for r in range(1, 4)
        for n in range(1, 5)
    ]
    await hall_repository.fill_hall(seats=seats)
    return Hall(hall_id=hall_id, hall_name=hall.hall_name, rows=hall.rows, seats_per_row=hall.seats_per_row)


@pytest.fixture
def reservation_repository(db_session: AsyncSession) -> IReservationRepository:
    return ReservationRepository(session=db_session)


@pytest.fixture
async def db_user(db_session: AsyncSession) -> int:
    auth_repo = AuthRepository(session=db_session)
    user = User(
        user_id=None,
        email="reservation_test@test.com",
        password="password123",
        first_name="Test",
        last_name="User",
    )
    user.hash_password()
    return await auth_repo.save_user(user=user)


@pytest.fixture
async def db_screening(
    db_movie: Movie,
    db_hall: Hall,
    screening_repository: IScreeningRepository,
    screening_seat_repository: IScreeningSeatRepository,
    hall_repository: IHallRepository,
) -> Screening:
    screening = Screening(
        screening_id=None,
        movie_id=db_movie.movie_id,
        hall_id=db_hall.hall_id,
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=1, minutes=100),
        price_normal=25,
        price_vip=35,
        status="scheduled",
    )
    [screening_id] = await screening_repository.create_screenings(screenings=[screening])

    seat_ids = await hall_repository.fetch_seat_ids(hall_id=db_hall.hall_id)
    screening_seats = [
        ScreeningSeat(screening_id=screening_id, seat_id=sid, reservation_id=None, status="free")
        for sid in seat_ids
    ]
    await screening_seat_repository.create_screening_seats(screening_seats=screening_seats)

    return Screening(
        screening_id=screening_id,
        movie_id=db_movie.movie_id,
        hall_id=db_hall.hall_id,
        starts_at=screening.starts_at,
        ends_at=screening.ends_at,
        price_normal=screening.price_normal,
        price_vip=screening.price_vip,
        status=screening.status,
    )
