from shared.db_client.base_orm import Base
from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String


class MovieORM(Base):
    __tablename__ = "movies"

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str]
    director: Mapped[str] = mapped_column(String(100))
    duration: Mapped[int]
    genre: Mapped[str] = mapped_column(String(50))
    rating: Mapped[float]
    poster_url: Mapped[str]

    __table_args__ = (
        Index("idx_movie_title", "title"),
        Index("idx_movie_genre", "genre"),
        Index("idx_movie_director", "director"),
        Index("idx_movie_rating", "rating"),
    )
