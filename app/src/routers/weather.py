from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies import get_cache_redis, get_db, rate_limit
from src.services import weather as weather_service

weather_router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)


@weather_router.get(
    "/current/{city}",
    summary="Get Current Weather",
    description="Fetches the current weather for a given city.",
    response_model=dict[str, Any],
)
async def get_current_weather(
    city: str,
    db: Session = Depends(get_db),
    r=Depends(get_cache_redis),
    _=Depends(rate_limit),
) -> dict[str, Any]:
    """
    - city: The name of the city.
    - db: Database session (dependency).
    - r: Redis cache session (dependency).
    - rate_limit: Rate limiter (dependency).
    """
    return await weather_service.fetch_current_weather(db, r, city)


@weather_router.get(
    "/forecast{city}",
    summary="Get Weather Forecast",
    description="Retrieves the weather forecast for the next `5` days.",
    response_model=dict[str, Any],
)
async def get_weather_forecast(
    city: str, days: int = 5, r=Depends(get_cache_redis), _=Depends(rate_limit)
) -> dict[str, Any]:
    """
    - city: The name of the city.
    - days: Number of days for the forecast (default: 5).
    - r: Redis cache session (dependency).
    - rate_limit: Rate limiter (dependency).
    """
    return await weather_service.fetch_weather_forecast(r, city, days)
