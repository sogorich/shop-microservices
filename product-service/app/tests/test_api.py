from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from conftest import client, db_session, create_new_product, mock_product_data, get_id_created_product
from database.models import Product
from repositories.repository import ProductRepository


async def test_create_product(client: AsyncClient, create_new_product):
    ...


async def test_create_product_and_get_id(client: AsyncClient, create_new_product, get_id_created_product):
    ...


async def test_get_product(
        client: AsyncClient, 
        db_session: AsyncSession, 
        create_new_product, 
        get_id_created_product, 
        mock_product_data):
    
    response = await client.get(f"/api/products/{get_id_created_product}")
    assert response.status_code == 200

    assert response.json()["title"] == mock_product_data["title"]
    assert response.json()["description"] == mock_product_data["description"]
    assert response.json()["photo_uri"] == mock_product_data["photo_uri"]
    assert response.json()["price"] == mock_product_data["price"]


async def test_update_product(
        client: AsyncClient, db_session: AsyncSession, 
        create_new_product, get_id_created_product, mock_product_data):

    repo = ProductRepository(db_session)
    res = await repo.update(id=get_id_created_product, data={"title": "Новый"})

    assert res.title != mock_product_data["title"]
    assert res.title == "Новый"

