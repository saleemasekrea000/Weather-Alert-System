from fastapi import FastAPI

from src.redis_client import r as redis_client
from src.routers import alert, weather

app = FastAPI()

app.include_router(weather.weather_router)
app.include_router(alert.alert_router)


@app.on_event("startup")
async def startup():
    # Initialize Redis connection when app starts.
    await redis_client.init()


@app.on_event("shutdown")
async def shutdown():
    # Close Redis connection when app stops.
    await redis_client.close()


@app.get("/")
def health_check():
    return {"status": "ok"}
