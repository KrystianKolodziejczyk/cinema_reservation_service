from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass(frozen=True)
class MovieData:
    title: str
    description: str
    director: str
    duration: int
    genre: str
    rating: float


@dataclass(frozen=True)
class SeatData:
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
    hall_name: str
    seats: list[SeatData]
