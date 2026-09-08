from abc import ABC, abstractmethod

from database.schemas import ProductCreate, ProductUpdate
from database.models import Product


class IService(ABC):
    """Интерфейс, устанавливающий контракт на реализацию сервисов"""
    @abstractmethod
    async def get_one(self, id: int) -> Product | None:
        ...

    @abstractmethod
    async def get_all(self) -> list[Product]:
        ...

    @abstractmethod
    async def create(self, payload: ProductCreate) -> Product:
        ...

    @abstractmethod
    async def update(self, id: int, update_model: ProductUpdate) -> Product | None:
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        ...