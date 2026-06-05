from app.modules.cinema.domain.entities import Seat
from app.modules.cinema.infrastructure.orm import SeatORM


class SeatMapper:
    @staticmethod
    def to_orm(seat: Seat) -> SeatORM:
        return SeatORM(
            seat_id=seat.seat_id,
            hall_id=seat.hall_id,
            row=seat.row,
            number=seat.number,
            seat_type=seat.seat_type,
        )

    @staticmethod
    def to_entity(seat_orm: SeatORM) -> Seat:
        return Seat(
            seat_id=seat_orm.seat_id,
            hall_id=seat_orm.hall_id,
            row=seat_orm.row,
            number=seat_orm.number,
            seat_type=seat_orm.seat_type,
        )
