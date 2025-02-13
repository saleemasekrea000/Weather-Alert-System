from sqlalchemy.orm import Session

from src.settings import base_settings
from src.utils.weather import send_request
from src.models.weather import Weather


async def fetch_current_weather(db: Session, city: str):
    url = f"{base_settings.weather_url}/weather"

    params = {
        "q": city,
        "appid": base_settings.weather_api_key,
    }
    weather_data = await send_request(url, params)
    store_weather_data(db, weather_data)
    return weather_data


async def fetch_weather_forecast(city: str, days: int = 5):

    url = f"{base_settings.weather_url}/forecast"

    params = {
        "q": city,
        "cnt": days,
        "appid": base_settings.weather_api_key,
    }
    return await send_request(url, params)


def store_weather_data(db: Session, weather_data: dict) -> None:
    weather = Weather(
        city=weather_data.get("name"),
        temperature=weather_data.get("main", {}).get("temp"),
        pressure=weather_data.get("main", {}).get("pressure"),
        humidity=weather_data.get("main", {}).get("humidity"),
        wind_speed=weather_data.get("wind", {}).get("speed"),
    )
    db.add(weather)
    db.commit()
    db.refresh(weather)
