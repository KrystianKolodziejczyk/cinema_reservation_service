from app.modules.cinema.domain.entities.movie import Movie
from app.modules.cinema.infrastructure.orm.movie_orm import MovieORM


class MovieMapper:
    @staticmethod
    def to_orm(movie: Movie) -> MovieORM:
        return MovieORM(
            movie_id=movie.movie_id,
            title=movie.title,
            description=movie.description,
            director=movie.director,
            duration=movie.duration,
            genre=movie.genre,
            rating=movie.rating,
            poster_url=movie.poster_url,
        )

    @staticmethod
    def to_entity(movie_orm: MovieORM) -> Movie:
        return Movie(
            movie_id=movie_orm.movie_id,
            title=movie_orm.title,
            description=movie_orm.description,
            director=movie_orm.director,
            duration=movie_orm.duration,
            genre=movie_orm.genre,
            rating=movie_orm.rating,
            poster_url=movie_orm.poster_url,
        )
