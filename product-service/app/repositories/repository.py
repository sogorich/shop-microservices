from typing import Any, Type, Generic

from sqlmodel import select, update, and_
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.generics import ModelT

from app.repositories.interfaces import IRepository


class SQLRepository(IRepository, Generic[ModelT]):  
    """Основной репозиторий для работы с базой данных"""
    def __init__(self, model: Type[ModelT], model_instance_id: int, db_session: AsyncSession) -> None:
        self._model = model
        self._model_instance_id = model_instance_id
        self._db_session = db_session

    @property
    def get_db_session(self) -> AsyncSession:
        return self._db_session

    @property
    def get_model(self) -> Type[ModelT]:
        return self._model

    @property
    def get_model_instance_id(self) -> int:
        return self._model_instance_id

    async def get_by_id(self, id: int) -> ModelT | None:
        return await self.get_db_session.get(self.get_model, id)

    async def get_all(self) -> list[ModelT]:
        query = await self.get_db_session.exec(select(self.get_model))
        return list(query.all())
    
    async def create(self, payload: ModelT) -> ModelT:
        new_product = self.get_model(**payload.model_dump())
        self.get_db_session.add(new_product)

        return new_product
    
    async def update(self, id: int, data: dict[str, Any]) -> ModelT:
        statement = update(self.get_model)\
            .where(and_(self.get_model_instance_id == id)).\
                values(**data).\
                    returning(self.get_model)
        
        updated_object = await self.get_db_session.exec(statement)
        return updated_object.scalars().one()

    async def delete(self, id: int) -> bool:
        model_instance = await self.get_by_id(id)

        if model_instance:
            await self.get_db_session.delete(model_instance)
            return True

        return False