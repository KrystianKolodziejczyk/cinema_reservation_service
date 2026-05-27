from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CHAR, CheckConstraint, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.shared.database_conn.base_orm import Base

if TYPE_CHECKING:
    from app.modules.auth.infrastructure.orm import UserORM
    from app.modules.cinema.infrastructure.orm import ReservedSeatORM, ScreeningORM


class ReservationORM(Base):
    __tablename__ = "reservations"

    reservation_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="RESTRICT")
    )
    screening_id: Mapped[int | None] = mapped_column(
        ForeignKey("screenings.screening_id", ondelete="SET NULL")
    )
    status: Mapped[str]
    total_price: Mapped[float]
    conf_code: Mapped[str] = mapped_column(CHAR(15))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped[UserORM] = relationship(back_populates="reservations")
    screening: Mapped[ScreeningORM] = relationship(back_populates="reservations")
    reserved_seats: Mapped[list[ReservedSeatORM]] = relationship(
        back_populates="reservation"
    )

    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_screening_id", "screening_id"),
        CheckConstraint(
            "status IN ('pending', 'confirmed', 'cancelled', 'expired')",
            name="ck_reservation_status",
        ),
    )
