import json
from unittest.mock import AsyncMock, patch

import httpx
import pytest
import respx
from sqlalchemy.orm import Session

from src.services.weather import fetch_current_weather
from src.settings import base_settings
from src.utils.weather import send_request


@pytest.mark.asyncio
async def test_send_request_success():
    url = "https://api.example.com"
    params = {"param": "value"}
    expected_json = {"key": "value"}

    # Use respx to mock the GET request.
    with respx.mock:
        route = respx.get(url, params=params).mock(
            return_value=httpx.Response(200, json=expected_json)
        )

        response = await send_request(url, params)

        assert response == expected_json
        assert route.called


@pytest.mark.asyncio
async def test_fetch_current_weather_cached_data(db_session: Session):
    city = "malaysia"
    fake_weather_data = {"temp": 15}

    """ Mock the Redis client to return cached data
        use AsyncMock because fetch_current_weather is an async function
        and redis operations not awaitable .
    """
    mock_r = AsyncMock()
    mock_r.get = AsyncMock(return_value=json.dumps(fake_weather_data))

    _ = await fetch_current_weather(db_session, mock_r, city)

    # Verify that the cached data is returned
    mock_r.get.assert_called_once_with(f"weather:current:{city.lower()}")

    # Ensure we didn't store anything in cache
    mock_r.set.assert_not_called()


@pytest.mark.asyncio
async def test_fetch_current_weather_no_cache(db_session):
    city = "malaysia"
    fake_weather_data = {
        "temp": 15,
    }
    cache_key = f"weather:current:{city.lower()}"

    mock_r = AsyncMock()

    # No cached data
    mock_r.get.return_value = None

    # Mock send_request to return fake weather data
    with patch(
        "src.services.weather.send_request", new_callable=AsyncMock
    ) as mock_send_request, patch(
        "src.services.weather.store_weather_data"
    ) as mock_store_weather_data:

        mock_send_request.return_value = fake_weather_data

        _ = await fetch_current_weather(db_session, mock_r, city)

        mock_send_request.assert_awaited_once()
        # Verify that the weather data was stored in the database.
        mock_store_weather_data.assert_called_once_with(db_session, fake_weather_data)
        # Verify that the data was cached.
        mock_r.set.assert_awaited_once_with(
            cache_key,
            json.dumps(fake_weather_data),
            ex=base_settings.current_weather_cache_ttl,
        )
