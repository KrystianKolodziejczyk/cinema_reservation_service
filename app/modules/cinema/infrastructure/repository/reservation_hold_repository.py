import json
from datetime import UTC, datetime, timedelta

from redis import Redis

from app.modules.cinema.application.dto import SeatHoldData
from app.modules.cinema.application.excpetions import PermissionDeniedError
from app.modules.cinema.infrastructure.interface import IReservationHoldRepository

HOLD_TTL_SECONDS = 600


class ReservationHoldRepository(IReservationHoldRepository):
    def __init__(self, redis_client: Redis) -> None:
        self._redis = redis_client

    async def hold(
        self,
        user_id: int,
        seat_ids: list[int],
        screening_id: int,
        seats_data: list[SeatHoldData],
    ) -> tuple[int, datetime]:
        hold_id = self._redis.incr("reservation_hold:counter")
        expires_at = datetime.now(tz=UTC) + timedelta(seconds=HOLD_TTL_SECONDS)

        payload = json.dumps(
            {
                "hold_id": hold_id,
                "user_id": user_id,
                "screening_id": screening_id,
                "seat_ids": seat_ids,
                "expires_at": expires_at.isoformat(),
            }
        )
        self._redis.set(f"reservation_hold:{hold_id}", payload, ex=HOLD_TTL_SECONDS)

        pipe = self._redis.pipeline()
        for seat_id in seat_ids:
            pipe.set(
                f"seat_hold:{screening_id}:{seat_id}",
                hold_id,
                ex=HOLD_TTL_SECONDS,
            )
        pipe.execute()

        return hold_id, expires_at

    async def release(self, hold_id: int, user_id: int, screening_id: int) -> bool:
        raw = self._redis.get(f"reservation_hold:{hold_id}")
        if not raw:
            return False

        data = json.loads(raw)

        if data["user_id"] != user_id:
            raise PermissionDeniedError(status_code=403, detail="Permission denied")

        if data["screening_id"] != screening_id:
            return False

        seat_ids = data["seat_ids"]
        pipe = self._redis.pipeline()
        pipe.delete(f"reservation_hold:{hold_id}")
        for seat_id in seat_ids:
            pipe.delete(f"seat_hold:{screening_id}:{seat_id}")
        pipe.execute()

        return True

    async def are_seats_held(self, screening_id: int, seat_ids: list[int]) -> list[int]:
        pipe = self._redis.pipeline()
        for seat_id in seat_ids:
            pipe.exists(f"seat_hold:{screening_id}:{seat_id}")
        results = pipe.execute()

        return [
            seat_id for seat_id, held in zip(seat_ids, results, strict=True) if held
        ]
