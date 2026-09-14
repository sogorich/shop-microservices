import pytest

from httpx import AsyncClient
from conftest import async_client


@pytest.mark.asyncio
async def test_hello(async_client: AsyncClient):
    response = await async_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"message": "Microservice \"product-service\" is ready!"}