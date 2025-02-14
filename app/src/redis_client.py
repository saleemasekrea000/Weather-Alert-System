import aioredis
from src.settings import base_settings


class RedisClient:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis = None

    async def init(self):
        # Initialize Redis connection.
        self.redis = await aioredis.from_url(self.redis_url, decode_responses=True)

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def get_redis(self):
        # Return Redis client instance.
        return self.redis


r = RedisClient(f"redis://{base_settings.redis_host}:{base_settings.redis_port}")
