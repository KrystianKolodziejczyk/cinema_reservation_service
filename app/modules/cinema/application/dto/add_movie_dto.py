from dataclasses import dataclass


@dataclass(frozen=True)
class AddMovieDTO:
    title: str
    description: str
    director: str
    duration: int
    genre: str
    rating: float
    poster_url: str | None = None
