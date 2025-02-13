import httpx
from fastapi import HTTPException


async def send_request(url: str, params: dict):
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
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
