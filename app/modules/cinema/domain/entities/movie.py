from dataclasses import dataclass


@dataclass
class Movie:
    movie_id: int | None
    title: str
    description: str
    director: str
    duration: int
    genre: str
    rating: float
    poster_url: str | None
