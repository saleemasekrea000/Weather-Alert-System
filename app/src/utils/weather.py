from typing import Any

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.weather import Weather


async def send_request(url: str, params: dict) -> dict[str, Any]:
    """
    Sends an asynchronous GET request to the specified URL with the provided parameters.

    Parameters:
        url (str): The target URL for the HTTP request.
        params (dict): The query parameters for the request.

    Returns:
        dict: The JSON response from the HTTP request.

    Raises:
        HTTPException: If the HTTP request fails with a status code error or encounters an unexpected error.
    """
    # Create an asynchronous HTTP client session using httpx.
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(url=url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=str(e.response.json().get("message")),
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


def store_weather_data(db: Session, weather_data: dict) -> None:
    """
    Stores or updates weather data in the database.

    Args:
        db (Session): SQLAlchemy database session.
        weather_data (dict): The weather data retrieved from the API.

    Process:
    - Checks if a weather record exists for the given city.
    - If the record exists, it updates the temperature, pressure, humidity, and wind speed.
    - If no record exists, it creates a new weather record and saves it.

    """
    city_name = weather_data.get("name").lower()
    # Try to fetch an existing weather record for this city
    weather = db.query(Weather).filter(Weather.city == city_name).first()

    if weather:
        # Update existing record
        weather.temperature = weather_data.get("main", {}).get("temp")
        weather.pressure = weather_data.get("main", {}).get("pressure")
        weather.humidity = weather_data.get("main", {}).get("humidity")
        weather.wind_speed = weather_data.get("wind", {}).get("speed")
    else:
        # Create new record
        weather = Weather(
            city=city_name,
            temperature=weather_data.get("main", {}).get("temp"),
            pressure=weather_data.get("main", {}).get("pressure"),
            humidity=weather_data.get("main", {}).get("humidity"),
            wind_speed=weather_data.get("wind", {}).get("speed"),
        )
        db.add(weather)

    db.commit()
    db.refresh(weather)
