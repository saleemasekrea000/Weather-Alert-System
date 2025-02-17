import json
from typing import Any

from sqlalchemy.orm import Session

from src.settings import base_settings
from src.utils.weather import send_request, store_weather_data


async def fetch_current_weather(db: Session, r, city: str) -> dict[str, Any]:
    """
    Fetch the current weather for a given city.

    - db (Session): Database session for storing weather data.
    - r: Redis cache instance for storing/retrieving cached weather data.
    - city (str): Name of the city to fetch the weather for.

    Process:
    1. Check if weather data for the city is cached in Redis.
    2. If cached data exists, return it.
    3. Otherwise, send a request to the weather API.
    4. Store the retrieved weather data in the database.
    5. Cache the weather data in Redis for future requests.

    Returns:
    - dict[str, Any]: The current weather data for the specified city.
    """
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

    """
    Fetch the weather forecast for a given city over a specified number of days.

    - r: Redis cache instance for storing/retrieving cached forecast data.
    - city (str): Name of the city to fetch the forecast for.
    - days (int, optional, default=5): Number of days for the forecast.

    Process:
    1. Check if forecast data for the city is cached in Redis.
    2. If cached data exists, return it.
    3. Otherwise, send a request to the weather API for forecast data.
    4. Cache the retrieved forecast data in Redis for future requests.

    Returns:
    - dict[str, Any]: The weather forecast data for the specified city and duration.
    """
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
