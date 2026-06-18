from datetime import datetime, timedelta

import pytest

from app.modules.cinema.domain.entities import Hall, Movie, Screening, ScreeningSeat
from app.modules.cinema.infrastructure.interface import (
    IScreeningRepository,
    IScreeningSeatRepository,
)

pytestmark = pytest.mark.anyio


class TestScreeningRepository:
    async def test_create_and_fetch_screening(
        self,
        screening_repository: IScreeningRepository,
        db_movie: Movie,
        db_hall: Hall,
    ):
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
        fetched = await screening_repository.fetch_basic_screening(screening_id=screening_id)

        assert fetched is not None
        assert fetched.screening_id == screening_id
        assert fetched.status == "scheduled"

    async def test_fetch_basic_screening_returns_none_when_not_found(
        self, screening_repository: IScreeningRepository
    ):
        result = await screening_repository.fetch_basic_screening(screening_id=99999)

        assert result is None

    async def test_fetch_screening_with_relations(
        self,
        screening_repository: IScreeningRepository,
        screening_seat_repository: IScreeningSeatRepository,
        hall_repository: IHallRepository,
        db_movie: Movie,
        db_hall: Hall,
    ):
        screening = Screening(
            screening_id=None,
            movie_id=db_movie.movie_id,
            hall_id=db_hall.hall_id,
            starts_at=datetime.now() + timedelta(days=2),
            ends_at=datetime.now() + timedelta(days=2, minutes=100),
            price_normal=20,
            price_vip=30,
            status="scheduled",
        )
        [screening_id] = await screening_repository.create_screenings(screenings=[screening])

        seat_ids = await hall_repository.fetch_seat_ids(hall_id=db_hall.hall_id)
        screening_seats = [
            ScreeningSeat(screening_id=screening_id, seat_id=sid, reservation_id=None, status="free")
            for sid in seat_ids
        ]
        await screening_seat_repository.create_screening_seats(screening_seats=screening_seats)

        result = await screening_repository.fetch_screening_with_relations(
            screening_id=screening_id
        )

        assert result is not None
        assert result.screening_id == screening_id
        assert result.movie.title == db_movie.title
        assert len(result.seats) == db_hall.rows * db_hall.seats_per_row

    async def test_fetch_screening_with_relations_returns_none_when_not_found(
        self, screening_repository: IScreeningRepository
    ):
        result = await screening_repository.fetch_screening_with_relations(
            screening_id=99999
        )

        assert result is None

    async def test_delete_screening_returns_true(
        self,
        screening_repository: IScreeningRepository,
        db_movie: Movie,
        db_hall: Hall,
    ):
        screening = Screening(
            screening_id=None,
            movie_id=db_movie.movie_id,
            hall_id=db_hall.hall_id,
            starts_at=datetime.now() + timedelta(days=3),
            ends_at=datetime.now() + timedelta(days=3, minutes=100),
            price_normal=20,
            price_vip=30,
            status="scheduled",
        )
        [screening_id] = await screening_repository.create_screenings(screenings=[screening])

        result = await screening_repository.delete_screening(screening_id=screening_id)

        assert result is True

    async def test_delete_screening_returns_false_when_not_found(
        self, screening_repository: IScreeningRepository
    ):
        result = await screening_repository.delete_screening(screening_id=99999)

        assert result is False
