from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.modules.cinema.application.dto import AddScreeningDTO, ScreeningDetailsDTO
from app.modules.cinema.application.dto.screening_details_dto import MovieData
from app.modules.cinema.application.service.screening_service import ScreeningService
from app.modules.cinema.application.dto.reservation_dto import (
    ReservationDTO,
    ReservationHallDTO,
    ReservationMovieDTO,
    ReservationScreeningDTO,
)
from app.modules.cinema.application.dto.reservation_hold_dto import HoldDTO, SeatHoldData
from app.modules.cinema.application.service.reservation_service import ReservationService
from app.modules.cinema.domain.entities import Screening
from app.modules.cinema.infrastructure.interface import (
    IHallRepository,
    IMovieRepository,
    IReservationHoldRepository,
    IReservationRepository,
    IScreeningRepository,
    IScreeningSeatRepository,
)


@pytest.fixture
def mock_movie_repository() -> AsyncMock:
    return AsyncMock(spec=IMovieRepository)


@pytest.fixture
def mock_hall_repository() -> AsyncMock:
    return AsyncMock(spec=IHallRepository)


@pytest.fixture
def mock_screening_repository() -> AsyncMock:
    return AsyncMock(spec=IScreeningRepository)


@pytest.fixture
def mock_screening_seat_repository() -> AsyncMock:
    return AsyncMock(spec=IScreeningSeatRepository)


@pytest.fixture
def mock_reservation_hold_repository() -> AsyncMock:
    return AsyncMock(spec=IReservationHoldRepository)


@pytest.fixture
def mock_reservation_repository() -> AsyncMock:
    return AsyncMock(spec=IReservationRepository)


@pytest.fixture
def reservation_service(
    mock_reservation_repository: AsyncMock,
    mock_reservation_hold_repository: AsyncMock,
    mock_screening_seat_repository: AsyncMock,
    mock_screening_repository: AsyncMock,
) -> ReservationService:
    return ReservationService(
        reservation_repository=mock_reservation_repository,
        redis_repository=mock_reservation_hold_repository,
        screening_seat_repository=mock_screening_seat_repository,
        screening_repository=mock_screening_repository,
    )


@pytest.fixture
def screening_service(
    mock_screening_repository: AsyncMock,
    mock_hall_repository: AsyncMock,
    mock_reservation_hold_repository: AsyncMock,
    mock_screening_seat_repository: AsyncMock,
    mock_movie_repository: AsyncMock,
) -> ScreeningService:
    return ScreeningService(
        screening_repository=mock_screening_repository,
        hall_repository=mock_hall_repository,
        redis_repository=mock_reservation_hold_repository,
        screening_seat_repository=mock_screening_seat_repository,
        movie_repository=mock_movie_repository,
    )


@pytest.fixture
def add_screening_dto() -> AddScreeningDTO:
    return AddScreeningDTO(
        movie_id=1,
        hall_id=1,
        starts_at=[datetime.now() + timedelta(days=1)],
        price_normal=25,
        price_vip=35,
    )


@pytest.fixture
def screening_details_dto() -> ScreeningDetailsDTO:
    return ScreeningDetailsDTO(
        screening_id=1,
        movie=MovieData(
            movie_id=1,
            title="Movie",
            description="Desc",
            director="Dir",
            duration=100,
            genre="drama",
            rating=4.0,
            poster_url=None,
        ),
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=1, minutes=100),
        status="scheduled",
        hall_name="Hall A",
        seats=[],
    )


@pytest.fixture
def hold_dto() -> HoldDTO:
    return HoldDTO(
        hold_id=1,
        user_id=1,
        screening_id=1,
        seat_ids=[1],
        seats=[SeatHoldData(seat_id=1, row=1, number=1, price=25, seat_type="normal")],
        total_price=25,
        expires_at=datetime.now() + timedelta(minutes=10),
    )


@pytest.fixture
def scheduled_screening() -> Screening:
    return Screening(
        screening_id=1,
        movie_id=1,
        hall_id=1,
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=1, minutes=100),
        price_normal=25,
        price_vip=35,
        status="scheduled",
    )


@pytest.fixture
def ongoing_screening() -> Screening:
    return Screening(
        screening_id=1,
        movie_id=1,
        hall_id=1,
        starts_at=datetime.now() - timedelta(hours=1),
        ends_at=datetime.now() + timedelta(hours=1),
        price_normal=25,
        price_vip=35,
        status="ongoing",
    )


@pytest.fixture
def reservation_dto() -> ReservationDTO:
    return ReservationDTO(
        reservation_id=1,
        user_id=2,
        status="confirmed",
        total_price=25,
        created_at=datetime.now(),
        screening=ReservationScreeningDTO(
            screening_id=1,
            starts_at=datetime.now(),
            ends_at=datetime.now(),
            status="scheduled",
            price_normal=25,
            price_vip=35,
            movie=ReservationMovieDTO(movie_id=1, title="Movie", poster_url=None),
            hall=ReservationHallDTO(hall_id=1, hall_name="Hall A"),
        ),
        seats=[],
    )
