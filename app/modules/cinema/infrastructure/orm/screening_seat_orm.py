from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.shared.database_conn.base_orm import Base

if TYPE_CHECKING:
    from app.modules.cinema.infrastructure.orm import (
        ReservationORM,
        ScreeningORM,
        SeatORM,
    )


class ScreeningSeatORM(Base):
    __tablename__ = "screening_seats"

    screening_id: Mapped[int] = mapped_column(
        ForeignKey("screenings.screening_id", ondelete="CASCADE"), primary_key=True
    )
    seat_id: Mapped[int] = mapped_column(
        ForeignKey("seats.seat_id", ondelete="CASCADE"), primary_key=True
    )
    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservations.reservation_id", ondelete="SET NULL")
    )
    status: Mapped[str] = mapped_column(default="free")

    seat: Mapped[SeatORM] = relationship(back_populates="screening_seat")
    screening: Mapped[ScreeningORM] = relationship(back_populates="screening_seats")
    reservation: Mapped[ReservationORM] = relationship(back_populates="screening_seats")

    __table_args__ = (
        CheckConstraint(
            "status IN ('free', 'reserved', 'cancelled')", name="ck_seat_status"
        ),
    )
