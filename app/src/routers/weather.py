from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.services import weather as weather_service
from src.dependencies import get_db

weather_router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)


@weather_router.get("/current/{city}")
async def get_current_weather(city: str, db: Session = Depends(get_db),):
    return await weather_service.fetch_current_weather(db, city)


@weather_router.get("/forecast{city}")
async def get_weather_forecast(city: str, days: int = 5):
    return await weather_service.fetch_weather_forecast(city, days)
