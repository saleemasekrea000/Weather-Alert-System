import httpx

from fastapi import HTTPException

from src.settings import base_settings
from src.utils.weather import send_request


async def fetch_current_weather(city: str):
    url = f"{base_settings.weather_url}/weather"

    params = {
        "q": city,
        "appid": base_settings.weather_api_key,
    }
    return await send_request(url, params)


async def fetch_weather_forecast(city: str, days: int = 5):

    url = f"{base_settings.weather_url}/forecast"

    params = {
        "q": city,
        "cnt": days,
        "appid": base_settings.weather_api_key,
    }
    return await send_request(url, params)
