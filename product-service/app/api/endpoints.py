from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path, HTTPException, status

from database.models import Product
from database.schemas import ProductCreate, ProductRead, ProductUpdate

from services.service import ProductService
from .dependencies import get_product_service


router = APIRouter(prefix="/api", tags=["Микросервис товаров и категорий"])


@router.post("/products", response_model=ProductRead)
async def create_new_product(
    product: Annotated[ProductCreate, Body()],
    product_service: Annotated[ProductService, Depends(get_product_service)]) -> Product:
    """Создаем новый товар"""

    return await product_service.create(product)


@router.patch("/products/{product_id}", response_model=ProductRead)
async def update_data_product(
    product_id: Annotated[int, Path()],
    product: Annotated[ProductUpdate, Body()],
    product_service: Annotated[ProductService, Depends(get_product_service)]) -> Product | None:
    """Обновляем данные товара"""

    return await product_service.update(id=product_id, update_model=product)


@router.get("/products", response_model=list[ProductRead])
async def get_all_products(
    product_service: Annotated[ProductService, Depends(get_product_service)]) -> list[Product]:
    """Получаем список всех товаров"""

    return await product_service.get_all()


@router.get("/products/{product_id}", response_model=ProductRead)
async def get_product_by_id(
    product_id: Annotated[int, Path()],
    product_service: Annotated[ProductService, Depends(get_product_service)]) -> Product:
    """Получаем товар по id"""

    product = await product_service.get_one(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "Нет данных!"})

    return product