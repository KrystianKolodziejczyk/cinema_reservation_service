from redis import Redis

from app.modules.shared.config.settings import settings

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True,
)


def get_redis_client() -> Redis:
    return redis_client
