from abc import ABC, abstractmethod
from typing import Any

from sqlmodel.ext.asyncio.session import AsyncSession

from database.models import Product
from database.schemas import ProductCreate


class IRepository(ABC):
    """Интерфейс, устанавливающий контракт на реализацию репозиториев"""
    @property
    @abstractmethod
    def get_db_session(self) -> AsyncSession:
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> Product | None:
        ...

    @abstractmethod
    async def get_all(self) -> list:
        ...

    @abstractmethod
    async def create(self, payload: ProductCreate) -> Product:
        ...

    @abstractmethod
    async def update(self, id: int, data: dict[str, Any]) -> Product:
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        ...