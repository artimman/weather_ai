# fastapi_app/app/utils/http_client.py
# Example of use:
# from app.utils.http_client import async_get
# weather = await async_get("https://api.weather.com/...")

import httpx


async def async_get(
    url: str, params: dict = None, headers: dict = None, timeout: int = 10
):
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()


async def async_post(url: str, json=None, headers: dict = None, timeout: int = 10):
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(url, json=json, headers=headers)
        r.raise_for_status()
        return r.json()
