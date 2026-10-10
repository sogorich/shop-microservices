from typing import Generic, Type

from app.services.interfaces import IService
from app.services.utils import get_404_exception

from app.database.generics import ModelT
from app.repositories.interfaces import IRepository


class ORMService(IService, Generic[ModelT]):
    """Базовый сервис. Реализует основные атрибуты для всех сервисов"""
    def __init__(self, model: Type[ModelT], repo: IRepository) -> None:
        self._model = model
        self._repo = repo

    @property
    def repo(self) -> IRepository:
        return self._repo

    @property
    def model(self) -> Type[ModelT]:
        return self._model

    async def get_one(self, id: int) -> ModelT | None:
            return await self.repo.get_by_id(id)
    
    async def get_all(self) -> list[ModelT]:
        return await self.repo.get_all()

    async def create(self, payload: ModelT) -> ModelT:
        new_product = await self.repo.create(payload)

        await self.repo.get_db_session.commit()
        await self.repo.get_db_session.refresh(new_product)

        return new_product

    async def update(self, id: int, update_model: ModelT) -> ModelT | None:
        product = await self.get_one(id=id)

        if not product:
            raise get_404_exception()

        product_data = update_model.model_dump(exclude_unset=True)
        updated_product = await self.repo.update(id=id, data=product_data) # TODO: check id column

        await self.repo.get_db_session.commit()
        await self.repo.get_db_session.refresh(updated_product)

        return updated_product

    async def delete(self, id: int) -> bool:
        delete_result = await self.repo.delete(id)

        if not delete_result:
            raise get_404_exception()

        await self.repo.get_db_session.commit()
        return True