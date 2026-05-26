from datetime import datetime
from typing import TYPE_CHECKING

from shared.database_conn.base_orm import Base
from sqlalchemy import CheckConstraint, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.cinema.infrastructure.orm import HallORM, MovieORM, ReservationORM


class ScreeningORM(Base):
    __tablename__ = "screenings"

    screening_id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.movie_id", ondelete="CASCADE")
    )
    hall_id: Mapped[int] = mapped_column(
        ForeignKey("halls.hall_id", ondelete="CASCADE")
    )
    starts_at: Mapped[datetime]
    price_normal: Mapped[int]
    price_vip: Mapped[int]
    status: Mapped[str]

    movie: Mapped[MovieORM] = relationship(back_populates="screenings")
    hall: Mapped[HallORM] = relationship(back_populates="screenings")
    reservations: Mapped[list[ReservationORM]] = relationship(
        back_populates="screening"
    )

    __table_args__ = (
        Index("idx_movie_id", "movie_id"),
        Index("idx_hall_id", "hall_id"),
        CheckConstraint(
            "status IN ('scheduled', 'ongoing', 'completed', 'canceled')",
            name="ck_screening_status",
        ),
    )
