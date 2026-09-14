from httpx import AsyncClient
from conftest import async_client


async def test_health_app(async_client: AsyncClient):
    response = await async_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"message": "Microservice \"product-service\" is ready!"}