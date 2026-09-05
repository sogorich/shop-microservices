from typing import Annotated
from fastapi import Depends

from services.service import ProductService
from repositories.repository import ProductRepository
from database.database import get_session

from sqlmodel.ext.asyncio.session import AsyncSession


def get_product_service(db_session: Annotated[AsyncSession, Depends(get_session)]) -> ProductService:
    """Возвращает объект сервиса модели товаров"""
    prod_repo = ProductRepository(db_session)
    return ProductService(prod_repo)