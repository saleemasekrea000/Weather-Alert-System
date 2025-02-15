import json
from typing import Any
from sqlalchemy.orm import Session

from src.settings import base_settings
from src.utils.weather import send_request, store_weather_data
from src.models.weather import Weather
from src.redis_client import r


async def fetch_current_weather(db: Session, r, city: str) -> dict[str, Any]:
    url = f"{base_settings.weather_url}/weather"

    params = {
        "q": city,
        "appid": base_settings.weather_api_key,
    }
    cache_key = f"weather:current:{city.lower()}"
    cached_data = await r.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    weather_data = await send_request(url, params)
    store_weather_data(db, weather_data)
    await r.set(
        cache_key, json.dumps(weather_data), ex=base_settings.current_weather_cache_ttl
    )
    return weather_data


async def fetch_weather_forecast(r, city: str, days: int = 5) -> dict[str, Any]:

    url = f"{base_settings.weather_url}/forecast"

    params = {
        "q": city,
        "cnt": days,
        "appid": base_settings.weather_api_key,
    }
    cache_key = f"weather:forecast:{city.lower()}"
    cached_data = await r.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    forecast_data = await send_request(url, params)
    await r.set(
        cache_key, json.dumps(forecast_data), ex=base_settings.forecast_cache_ttl
    )
    return forecast_data
