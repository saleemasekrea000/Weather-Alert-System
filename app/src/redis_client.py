from redis.asyncio import Redis

from src.settings import base_settings


class RedisClient:
    def __init__(self, redis_url: str, cache_db: int = 0, rate_limit_db: int = 1):
        """
        Initializes Redis client with separate databases for caching and rate limiting.

        :param redis_url: Redis connection URL
        :param cache_db: Redis database index for caching (default: 0)
        :param rate_limit_db: Redis database index for rate limiting (default: 1)
        """
        self.redis_url = redis_url
        self.cache_db = cache_db
        self.rate_limit_db = rate_limit_db
        self.cache_redis = None
        self.rate_limit_redis = None

    async def init(self):
        """Initialize Redis connections for caching and rate limiting."""
        self.cache_redis = await Redis.from_url(
            self.redis_url, db=self.cache_db, decode_responses=True
        )
        self.rate_limit_redis = await Redis.from_url(
            self.redis_url, db=self.rate_limit_db, decode_responses=True
        )

    async def close(self):
        if self.cache_redis:
            await self.cache_redis.close()
        if self.rate_limit_redis:
            await self.rate_limit_redis.close()

    async def get_cache_redis(self):
        return self.cache_redis

    async def get_rate_limit_redis(self):
        return self.rate_limit_redis


r = RedisClient(f"redis://{base_settings.redis_host}:{base_settings.redis_port}")
