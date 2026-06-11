from app.modules.cinema.domain.entities import ScreeningSeat
from app.modules.cinema.infrastructure.orm import ScreeningSeatORM


class ScreeningSeatMapper:
    @staticmethod
    def to_orm(screening_seat: ScreeningSeat) -> ScreeningSeatORM:
        return ScreeningSeatORM(
            screening_id=screening_seat.screening_id,
            seat_id=screening_seat.seat_id,
            reservation_id=screening_seat.reservation_id,
            status=screening_seat.status,
        )

    @staticmethod
    def to_entity(screening_seat_orm: ScreeningSeatORM) -> ScreeningSeat:
        return ScreeningSeat(
            screening_id=screening_seat_orm.screening_id,
            seat_id=screening_seat_orm.seat_id,
            reservation_id=screening_seat_orm.reservation_id,
            status=screening_seat_orm.status,
        )
