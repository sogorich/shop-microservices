from typing import Any

from sqlmodel import select, update, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from database.schemas import CategoryReadOrCreate, ProductCreate
from database.models import Category, Product

from .interfaces import IRepository


class BaseRepository:  
    """Базовый репозиторий. Реализует основные атрибуты для всех репозиториев"""
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    @property
    def get_db_session(self) -> AsyncSession:
        return self._db_session


class CategoryRepository(BaseRepository, IRepository):
    """Реализация контракт IRepository. Репозиторий категорий для работы с базой данных"""
    async def get_by_id(self, id: int) -> Category | None:
        query = await self.get_db_session.exec(select(Category).where(Category.id == id))
        return query.first()

    async def create(self, payload: CategoryReadOrCreate) -> Category:
        new_category = Category(**payload.model_dump())
        self.get_db_session.add(new_category)

        return new_category
    
    async def get_all(self) -> list[Category]:
        ...
    
    async def update(self, id: int, data: dict[str, Any]) -> Category:
        ...

    async def delete(self, id: int) -> bool:
        ...


class ProductRepository(BaseRepository, IRepository):
    """Реализация контракт IRepository. Репозиторий товаров для работы с базой данных"""
    async def get_by_id(self, id: int) -> Product | None:
        query = await self.get_db_session.exec(select(Product).where(Product.id == id))
        return query.first()

    async def get_all(self) -> list[Product]:
        query = await self.get_db_session.exec(select(Product))
        return list(query.all())
    
    async def create(self, payload: ProductCreate) -> Product:
        new_product = Product(**payload.model_dump())
        self.get_db_session.add(new_product)

        return new_product
    
    async def update(self, id: int, data: dict[str, Any]) -> Product:
        statement = update(Product)\
            .where(and_(Product.id == id)).\
                values(**data).\
                    returning(Product)
        
        updated_object = await self.get_db_session.exec(statement)
        return updated_object.scalars().one()

    async def delete(self, id: int) -> bool:
        product = await self.get_by_id(id)

        if product:
            await self.get_db_session.delete(product)
            return True

        return False