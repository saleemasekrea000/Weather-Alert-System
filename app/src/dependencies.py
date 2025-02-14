from src.database import SessionLocal
from src.redis_client import r


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_redis():
    return await r.get_redis()
