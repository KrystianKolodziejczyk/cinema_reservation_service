from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.shared.database_conn.base_orm import Base

if TYPE_CHECKING:
    from app.modules.auth.infrastructure.orm import UserORM
    from app.modules.cinema.infrastructure.orm import (
        ReservedSeatORM,
        ScreeningORM,
        ScreeningSeatORM,
    )


class ReservationORM(Base):
    __tablename__ = "reservations"

    reservation_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="RESTRICT")
    )
    screening_id: Mapped[int | None] = mapped_column(
        ForeignKey("screenings.screening_id", ondelete="SET NULL")
    )
    _status: Mapped[str] = mapped_column("status", default="confirmed")
    total_price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped[UserORM] = relationship(back_populates="reservations")
    screening: Mapped[ScreeningORM] = relationship(back_populates="reservations")
    reserved_seats: Mapped[list[ReservedSeatORM]] = relationship(
        back_populates="reservation"
    )
    screening_seats: Mapped[list[ScreeningSeatORM]] = relationship(
        back_populates="reservation"
    )

    @property
    def status(self) -> str:
        if self._status == "cancelled":
            return "cancelled"
        if self.screening is None or self.screening.ends_at < datetime.now(tz=UTC):
            return "expired"
        return "confirmed"

    __table_args__ = (
        Index("idx_reservations_user_id", "user_id"),
        Index("idx_reservations_screening_id", "screening_id"),
        CheckConstraint(
            "status IN ('confirmed', 'cancelled')",
            name="ck_reservation_status",
        ),
    )
