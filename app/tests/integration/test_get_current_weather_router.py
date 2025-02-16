from unittest.mock import patch

import pytest


@pytest.mark.asyncio
async def test_get_current_weather(client):
    city = "malaysia"
    fake_weather_data = {"temp": 15}

    # Mocking the fetch_current_weather method
    with patch(
        "src.services.weather.fetch_current_weather", return_value=fake_weather_data
    ):
        response = client.get(f"/weather/current/{city}")

        assert response.status_code == 200
        assert response.json() == fake_weather_data


@pytest.mark.asyncio
async def test_get_weather_forecast(client):
    city = "malaysia"
    days = 5
    fake_forecast_data = {"forecast": [{"day": 1, "temp": 15}, {"day": 2, "temp": 16}]}

    # Mocking the fetch_weather_forecast method
    with patch(
        "src.services.weather.fetch_weather_forecast", return_value=fake_forecast_data
    ):
        response = client.get(f"/weather/forecast{city}?days={days}")

        assert response.status_code == 200
        assert response.json() == fake_forecast_data
