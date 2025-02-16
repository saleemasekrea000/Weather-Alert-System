from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.redis_client import r as redis_client
from src.routers import alert, weather


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await redis_client.init()

    # Yield control back to FastAPI
    yield

    await redis_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(weather.weather_router)
app.include_router(alert.alert_router)


@app.get("/")
def health_check():
    return {"status": "ok"}
