from abc import ABC, abstractmethod
from typing import Any, Generic

from database.generics import ModelT
from sqlmodel.ext.asyncio.session import AsyncSession


class IRepository(ABC, Generic[ModelT]):
    """Интерфейс, устанавливающий контракт на реализацию репозиториев"""
    @property
    @abstractmethod
    def get_db_session(self) -> AsyncSession:
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> ModelT | None:
        ...

    @abstractmethod
    async def get_all(self) -> list:
        ...

    @abstractmethod
    async def create(self, payload: ModelT) -> ModelT:
        ...

    @abstractmethod
    async def update(self, id: int, data: dict[str, Any]) -> ModelT:
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        ...