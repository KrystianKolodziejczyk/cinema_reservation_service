from datetime import datetime

from sqlalchemy import ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.auth.infrastructure.orm import UserORM
from app.modules.shared.database_conn.base_orm import Base


class RefreshTokenORM(Base):
    __tablename__ = "refresh_tokens"

    refresh_token_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    token_hash: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped[UserORM] = relationship(back_populates="refresh_tokens")

    __table_args__ = (Index("idx_user_id", "user_id"),)
