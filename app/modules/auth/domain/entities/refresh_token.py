from dataclasses import dataclass
from datetime import datetime


@dataclass
class RefreshToken:
    refresh_token_id: int | None
    user_id: int
    token_hash: str
    expires_at: datetime
