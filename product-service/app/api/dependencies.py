from typing import Annotated
from fastapi import Depends

from services.service import CategoryService, ProductService
from repositories.repository import CategoryRepository, ProductRepository
from database.database import get_session

from sqlmodel.ext.asyncio.session import AsyncSession


def get_product_service(db_session: Annotated[AsyncSession, Depends(get_session)]) -> ProductService:
    """Возвращает объект сервиса модели товаров"""
    prod_repo = ProductRepository(db_session)
    return ProductService(prod_repo)


def get_category_service(db_session: Annotated[AsyncSession, Depends(get_session)]) -> CategoryService:
    """Возвращает объект сервиса модели категорий"""
    cat_repo = CategoryRepository(db_session)
    return CategoryService(cat_repo)