from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.shared.database_conn.base_orm import Base

if TYPE_CHECKING:
    from app.modules.cinema.infrastructure.orm import (
        HallORM,
        MovieORM,
        ReservationORM,
        ScreeningSeatORM,
    )


class ScreeningORM(Base):
    __tablename__ = "screenings"

    screening_id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.movie_id", ondelete="CASCADE")
    )
    hall_id: Mapped[int] = mapped_column(
        ForeignKey("halls.hall_id", ondelete="CASCADE")
    )
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    price_normal: Mapped[int]
    price_vip: Mapped[int]
    _status: Mapped[str] = mapped_column("status", default="scheduled")

    movie: Mapped[MovieORM] = relationship(back_populates="screenings")
    hall: Mapped[HallORM] = relationship(back_populates="screenings")
    reservations: Mapped[list[ReservationORM]] = relationship(
        back_populates="screening"
    )
    screening_seats: Mapped[list[ScreeningSeatORM]] = relationship(
        back_populates="screening"
    )

    @property
    def status(self) -> str:
        if self._status == "cancelled":
            return "cancelled"
        if self.starts_at > datetime.now(UTC):
            return "scheduled"
        if self.starts_at < datetime.now(UTC) < self.ends_at:
            return "ongoing"
        return "completed"

    __table_args__ = (
        Index("idx_movie_id", "movie_id"),
        Index("idx_hall_id", "hall_id"),
        CheckConstraint(
            "status IN ('scheduled', 'cancelled')",
            name="ck_screening_status",
        ),
    )
