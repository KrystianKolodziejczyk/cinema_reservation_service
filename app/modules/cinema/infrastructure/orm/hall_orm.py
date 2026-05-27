from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.shared.database_conn.base_orm import Base

if TYPE_CHECKING:
    from app.modules.cinema.infrastructure.orm import ScreeningORM, SeatORM


class HallORM(Base):
    __tablename__ = "halls"

    hall_id: Mapped[int] = mapped_column(primary_key=True)
    hall_name: Mapped[str] = mapped_column(String(15), unique=True)
    rows: Mapped[int]
    seats_per_row: Mapped[int]

    seats: Mapped[list[SeatORM]] = relationship(back_populates="hall")
    screenings: Mapped[list[ScreeningORM]] = relationship(back_populates="hall")

    __table_args__ = (
        CheckConstraint("rows > 0 AND rows <= 15", name="ck_rows_count"),
        CheckConstraint(
            "LENGTH(hall_name) > 0 AND LENGTH(hall_name) <= 15", name="ck_hall_name"
        ),
        CheckConstraint(
            "seats_per_row > 0 AND seats_per_row <= 20", name="ck_hall_seats_per_row"
        ),
    )
