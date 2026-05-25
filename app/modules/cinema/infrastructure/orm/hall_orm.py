from shared.db_client.base_orm import Base
from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class HallORM(Base):
    __tablename__ = "halls"

    hall_id: Mapped[int] = mapped_column(primary_key=True)
    hall_name: Mapped[str] = mapped_column(String(10), unique=True)
    rows: Mapped[int] = mapped_column(Integer)
    seats_per_row: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        CheckConstraint("rows > 0 AND rows <= 15", "ck_rows_count"),
        CheckConstraint(
            "LENGTH(hall_name) > 0 AND LENGTH(hall_name) <= 15", "ck_hall_name"
        ),
    )
