from app.modules.cinema.domain.entities.screening import Screening
from app.modules.cinema.infrastructure.orm.screening_orm import ScreeningORM


class ScreeningMapper:
    @staticmethod
    def to_entity(screening_orm: ScreeningORM) -> Screening:
        return Screening(
            screening_id=screening_orm.screening_id,
            movie_id=screening_orm.movie_id,
            hall_id=screening_orm.hall_id,
            starts_at=screening_orm.starts_at,
            ends_at=screening_orm.ends_at,
            price_normal=screening_orm.price_normal,
            price_vip=screening_orm.price_vip,
            status=screening_orm._status,
        )

    def to_orm(screening: Screening) -> ScreeningORM:
        return ScreeningORM(
            screening_id=screening.screening_id,
            movie_id=screening.movie_id,
            hall_id=screening.hall_id,
            starts_at=screening.starts_at,
            ends_at=screening.ends_at,
            price_normal=screening.price_normal,
            price_vip=screening.price_vip,
            _status=screening.status,
        )
