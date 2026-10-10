from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.responses import JSONResponse

from app.database.models import Category, Product
from app.database.schemas import CategoryReadOrCreate, ProductCreate, ProductRead, ProductUpdate

from app.services.service import ORMService
from app.services.utils import get_404_exception
from app.api.dependencies import get_category_service, get_product_service


router = APIRouter(prefix="/api", tags=["Микросервис товаров и категорий"])


@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_new_product(
    product: Annotated[ProductCreate, Body()],
    product_service: Annotated[ORMService, Depends(get_product_service)]) -> Product:
    """Создаем новый товар"""

    return await product_service.create(product)


@router.patch("/products/{product_id}", response_model=ProductRead)
async def update_data_product(
    product_id: Annotated[int, Path()],
    product: Annotated[ProductUpdate, Body()],
    product_service: Annotated[ORMService, Depends(get_product_service)]) -> Product | None:
    """Обновляем данные товара"""

    return await product_service.update(id=product_id, update_model=product)


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: Annotated[int, Path()],
    product_service: Annotated[ORMService, Depends(get_product_service)]) -> JSONResponse:
    """Удаляем товар по id"""
    await product_service.delete(product_id)
    return JSONResponse(content={"message": "Success"})


@router.get("/products", response_model=list[ProductRead])
async def get_all_products(
    product_service: Annotated[ORMService, Depends(get_product_service)]) -> list[Product]:
    """Получаем список всех товаров"""

    return await product_service.get_all()


@router.get("/products/{product_id}", response_model=ProductRead)
async def get_product_by_id(
    product_id: Annotated[int, Path()],
    product_service: Annotated[ORMService, Depends(get_product_service)]) -> Product:
    """Получаем товар по id"""

    product = await product_service.get_one(product_id)

    if not product:
        raise get_404_exception()

    return product


@router.get("/categories/{category_id}", response_model=CategoryReadOrCreate, response_model_exclude={"comment"})
async def get_category_by_id(
    category_id: Annotated[int, Path()],
    category_service: Annotated[ORMService, Depends(get_category_service)]) -> Category:
    """Получаем категорию по id"""

    category = await category_service.get_one(category_id)

    if not category:
        raise get_404_exception()

    return category


@router.post("/categories", response_model=CategoryReadOrCreate, status_code=status.HTTP_201_CREATED)
async def create_new_category(
    category: Annotated[CategoryReadOrCreate, Body()],
    category_service: Annotated[ORMService, Depends(get_category_service)]) -> Category:
    """Создаем новую категорию"""

    return await category_service.create(category)