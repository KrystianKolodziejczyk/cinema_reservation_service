from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass(frozen=True)
class MovieData:
    movie_id: int
    title: str
    description: str
    director: str
    duration: int
    genre: str
    rating: float
    poster_url: str | None


@dataclass(frozen=True)
class SeatData:
    seat_id: int
    row: int
    number: int
    seat_type: Literal["normal", "vip"]
    status: Literal["free", "reserved", "cancelled"]
    price: int


@dataclass(frozen=True)
class ScreeningDetailsDTO:
    screening_id: int
    movie: MovieData
    starts_at: datetime
    ends_at: datetime
    status: Literal["scheduled", "ongoing", "cancelled", "completed"]
    hall_name: str
    seats: list[SeatData]
