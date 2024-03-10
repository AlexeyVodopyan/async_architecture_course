# stdlib
from functools import cache

# thirdparty
from redis.asyncio import Redis

# project
from src.accounting.settings.config import settings


@cache
def get_redis_client() -> Redis:
    client = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        decode_responses=True,
    )

    return client
