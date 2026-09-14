from httpx import AsyncClient
from conftest import async_client


async def test_create_product(async_client: AsyncClient):
    response = await async_client.post("/api/products", json={
        "title": "First",
        "description": "Some",
        "photo_uri": "uri",
        "price": 1000
    })

    assert response.status_code == 201
    assert response.json() == {
            "title": "First",
            "description": "Some",
            "photo_uri": "uri",
            "price": 1000,
            "category": None
    }
