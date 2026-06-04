from app.modules.cinema.domain.entities import Hall
from app.modules.cinema.infrastructure.orm import HallORM


class HallMapper:
    @staticmethod
    def to_orm(hall: Hall) -> HallORM:
        return HallORM(
            hall_id=hall.hall_id,
            hall_name=hall.hall_name,
            rows=hall.rows,
            seats_per_row=hall.seats_per_row,
        )

    @staticmethod
    def to_entity(hall_orm: HallORM) -> Hall:
        return Hall(
            hall_id=hall_orm.hall_id,
            hall_name=hall_orm.hall_name,
            rows=hall_orm.rows,
            seats_per_row=hall_orm.seats_per_row,
        )
