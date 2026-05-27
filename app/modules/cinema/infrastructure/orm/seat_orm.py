from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.shared.database_conn.base_orm import Base

if TYPE_CHECKING:
    from app.modules.cinema.infrastructure.orm import HallORM, ReservedSeatORM


class SeatORM(Base):
    __tablename__ = "seats"

    seat_id: Mapped[int] = mapped_column(primary_key=True)
    hall_id: Mapped[int] = mapped_column(
        ForeignKey("halls.hall_id", ondelete="CASCADE")
    )
    row: Mapped[int]
    number: Mapped[int]
    seat_type: Mapped[str] = mapped_column(default="normal")

    hall: Mapped[HallORM] = relationship(back_populates="seats")
    reserved_seats: Mapped[list[ReservedSeatORM]] = relationship(back_populates="seat")

    __table_args__ = (
        Index("idx_seat_row", "row"),
        Index("idx_seat_number", "number"),
        CheckConstraint("row > 0 AND row <= 15", name="ck_seat_row"),
        CheckConstraint("number > 0 AND number <= 20", name="ck_seat_number"),
        CheckConstraint("seat_type IN ('normal', 'vip')", name="ck_seat_type"),
    )
