import time

from fastapi import Depends, HTTPException, Request

from src.database import SessionLocal
from src.redis_client import r
from src.settings import base_settings


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# here not using yeild because we dont need to close the connection every time
# we can use the same connection for multiple requests
async def get_cache_redis():
    return await r.get_cache_redis()


async def get_rate_limit_redis():
    return await r.get_rate_limit_redis()


async def rate_limit(request: Request, r=Depends(get_rate_limit_redis)) -> None:
    """
    Allows up to 60 requests per minute across all users.
    Uses Redis to count requests in the current minute and raises
    HTTP 429 if the limit is exceeded.
    """
    current_window = int(time.time() // base_settings.rate_limit_window)

    # each endpoint has its own rate limit
    endpoint_url = request.url.path

    # Key format: rate_limit:<current_window>
    key = f"{endpoint_url}:{current_window}"

    # Increment the counter for the current minute
    count = await r.incr(key)

    # Set the key to expire after the window (first request only)
    if count == 1:
        await r.expire(key, base_settings.rate_limit_window)

    if count > base_settings.rate_limit_count:
        raise HTTPException(
            status_code=429, detail="Too Many Requests. Please try again later."
        )
