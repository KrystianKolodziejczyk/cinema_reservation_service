from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from app.modules.cinema.domain.entities.seat import Seat


@dataclass(frozen=True)
class ReservationMovieDTO:
    movie_id: int
    title: str
    poster_url: str | None


@dataclass(frozen=True)
class ReservationHallDTO:
    hall_id: int
    hall_name: str


@dataclass(frozen=True)
class ReservationScreeningDTO:
    screening_id: int | None
    starts_at: datetime
    ends_at: datetime
    status: str
    price_normal: int
    price_vip: int
    movie: ReservationMovieDTO
    hall: ReservationHallDTO


@dataclass(frozen=True)
class ReservationDTO:
    reservation_id: int | None
    user_id: int
    status: Literal["pending", "confirmed", "cancelled", "expired"]
    total_price: int
    created_at: datetime
    screening: ReservationScreeningDTO
    seats: list[Seat]
