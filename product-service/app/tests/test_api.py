from httpx import AsyncClient
from conftest import client


async def test_create_product(client: AsyncClient):

    data = {
        "title": "Second",
        "description": "Some",
        "photo_uri": "http://localhost:8000/some_photo",
        "price": 1000
    }

    response = await client.post("/api/products", json=data)

    assert response.status_code == 201

    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert response.json()["photo_uri"] == data["photo_uri"]
    assert response.json()["price"] == data["price"]