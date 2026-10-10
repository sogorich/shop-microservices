from typing import Annotated
from fastapi import Depends

from app.services.service import ORMService
from app.repositories.repository import SQLRepository

from app.database.database import get_session
from app.database.models import Category, Product

from sqlmodel.ext.asyncio.session import AsyncSession


def get_product_service(db_session: Annotated[AsyncSession, Depends(get_session)]) -> ORMService:
    """Возвращает объект сервиса модели товаров"""
    prod_repo = SQLRepository(Product, Product.id, db_session)
    return ORMService(Product, prod_repo)


def get_category_service(db_session: Annotated[AsyncSession, Depends(get_session)]) -> ORMService:
    """Возвращает объект сервиса модели категорий"""
    prod_repo = SQLRepository(Category, Category.id, db_session)
    return ORMService(Category, prod_repo)