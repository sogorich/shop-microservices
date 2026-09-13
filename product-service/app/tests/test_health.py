import pytest

from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_hello():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://") as ac:
        response = await ac.get("/health")

    assert response.status_code == 200
    assert response.json() == {"message": "Microservice \"product-service\" is ready!"}