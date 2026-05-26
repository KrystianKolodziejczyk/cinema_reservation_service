from datetime import datetime
from typing import TYPE_CHECKING

from shared.database_conn.base_orm import Base
from sqlalchemy import CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.cinema.infrastructure.orm import ReservationORM


class UserORM(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    reservations: Mapped[list[ReservationORM]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint("LENGTH(first_name) > 2", name="ck_user_first_name"),
        CheckConstraint("LENGTH(last_name) > 2", name="ck_user_last_name"),
    )
