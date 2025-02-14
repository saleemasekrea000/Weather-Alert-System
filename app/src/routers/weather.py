from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.services import weather as weather_service
from src.dependencies import get_db, get_redis

weather_router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)


@weather_router.get("/current/{city}")
async def get_current_weather(
    city: str, db: Session = Depends(get_db), r=Depends(get_redis)
):
    return await weather_service.fetch_current_weather(db, r, city)


@weather_router.get("/forecast{city}")
async def get_weather_forecast(city: str, days: int = 5, r=Depends(get_redis)):
    return await weather_service.fetch_weather_forecast(r, city, days)
