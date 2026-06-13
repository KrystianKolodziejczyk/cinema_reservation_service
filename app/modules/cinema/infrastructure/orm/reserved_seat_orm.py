from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.shared.database_conn.base_orm import Base

if TYPE_CHECKING:
    from app.modules.cinema.infrastructure.orm import ReservationORM, SeatORM


class ReservedSeatORM(Base):
    __tablename__ = "reserved_seats"

    seat_id: Mapped[int] = mapped_column(
        ForeignKey("seats.seat_id", ondelete="RESTRICT"), primary_key=True
    )
    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservations.reservation_id", ondelete="CASCADE"), primary_key=True
    )
    price_paid: Mapped[float]

    reservation: Mapped[ReservationORM] = relationship(back_populates="reserved_seats")
    seat: Mapped[SeatORM] = relationship(back_populates="reserved_seats")
