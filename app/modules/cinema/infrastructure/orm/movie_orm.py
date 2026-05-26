from shared.db_client.base_orm import Base
from sqlalchemy import CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String


class MovieORM(Base):
    __tablename__ = "movies"

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(default=None)
    director: Mapped[str] = mapped_column(String(100))
    duration: Mapped[int]
    genre: Mapped[str] = mapped_column(String(50))
    rating: Mapped[float | None] = mapped_column(default=None)
    poster_url: Mapped[str | None] = mapped_column(default=None)

    __table_args__ = (
        Index("idx_movie_title", "title"),
        Index("idx_movie_genre", "genre"),
        Index("idx_movie_director", "director"),
        Index("idx_movie_rating", "rating"),
        CheckConstraint("LENGTH(title) > 2", name="ck_movie_title"),
        CheckConstraint("duration > 0", name="ck_movie_duration"),
        CheckConstraint("rating >= 0.0 AND rating <= 5.0", name="ck_movie_rating"),
        CheckConstraint(
            "LENGTH(description) > 2 AND LENGTH(description) <= 500",
            name="ck_movie_descritpion",
        ),
    )
