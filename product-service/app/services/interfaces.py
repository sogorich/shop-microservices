from abc import ABC, abstractmethod
from typing import Generic

from app.database.generics import ModelT


class IService(ABC, Generic[ModelT]):
    """Интерфейс, устанавливающий контракт на реализацию сервисов"""
    @abstractmethod
    async def get_one(self, id: int) -> ModelT | None:
        ...

    @abstractmethod
    async def get_all(self) -> list[ModelT]:
        ...

    @abstractmethod
    async def create(self, payload: ModelT) -> ModelT:
        ...

    @abstractmethod
    async def update(self, id: int, update_model: ModelT) -> ModelT | None:
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        ...