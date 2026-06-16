from app.modules.cinema.domain.entities.reservation import Reservation
from app.modules.cinema.infrastructure.orm.reservation_orm import ReservationORM


class ReservationMapper:
    @staticmethod
    def to_orm(reservation: Reservation) -> ReservationORM:
        return ReservationORM(
            reservation_id=reservation.reservation_id,
            user_id=reservation.user_id,
            screening_id=reservation.screening_id,
            _status=reservation.status,
            total_price=reservation.total_price,
            conf_code=reservation.conf_code,
        )

    def to_entity(reservation_orm: ReservationORM) -> Reservation:
        return Reservation(
            reservation_id=reservation_orm.reservation_id,
            user_id=reservation_orm.user_id,
            screening_id=reservation_orm.screening_id,
            status=reservation_orm.status,
            total_price=reservation_orm.total_price,
            conf_code=reservation_orm.conf_code,
        )
