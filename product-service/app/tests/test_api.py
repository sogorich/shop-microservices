from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from conftest import client, db_session
from database.models import Product


data = {
    "title": "Second",
    "description": "Some",
    "photo_uri": "http://localhost:8000/some_photo",
    "price": 1000
}


async def test_create_product(client: AsyncClient):

    response = await client.post("/api/products", json=data)

    assert response.status_code == 201

    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert response.json()["photo_uri"] == data["photo_uri"]
    assert response.json()["price"] == data["price"]


async def test_get_product(client: AsyncClient, db_session: AsyncSession):

    create_response = await client.post("/api/products", json=data)
    assert create_response.status_code == 201

    statement = select(Product).where(Product.title == data["title"])
    scalar_result = await db_session.exec(statement)
    product = scalar_result.first()

    assert product is not None
    assert product.id > 0

    response = await client.get(f"/api/products/{product.id}")
    assert response.status_code == 200

    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert response.json()["photo_uri"] == data["photo_uri"]
    assert response.json()["price"] == data["price"]