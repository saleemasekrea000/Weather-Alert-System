from src.database import SessionLocal
from src.redis_client import r


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# here not using yeild because we dont need to close the connection every time
# we can use the same connection for multiple requests
async def get_redis():
    return await r.get_redis()
