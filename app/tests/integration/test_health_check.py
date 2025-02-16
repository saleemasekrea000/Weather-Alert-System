import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app

# https://fastapi.tiangolo.com/advanced/async-tests/?query=integration+test#in-detail
# ASGITransport communicates directly with the FastAPI application (app)
#  in memory without sending a real HTTP request.
@pytest.mark.anyio
async def test_root():
    # AsyncClient is the mocked request.
    async with AsyncClient(
        # Use ASGITransport to test the ASGI app
        # no need to make a real HTTP request (faster)
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
