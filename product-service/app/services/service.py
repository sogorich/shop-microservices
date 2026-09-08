from .interfaces import IService
from .utils import get_404_exception

from database.models import Product
from database.schemas import ProductCreate, ProductUpdate

from repositories.interfaces import IRepository


class ProductService(IService):
    """Реализует контракт IService. Сервис для работы с моделью продуктов"""
    def __init__(self, repo: IRepository) -> None:
        self._repo = repo

    async def get_one(self, id: int) -> Product | None:
        return await self._repo.get_by_id(id)

    async def get_all(self) -> list[Product]:
        return await self._repo.get_all()

    async def create(self, payload: ProductCreate) -> Product:
        new_product = await self._repo.create(payload)

        await self._repo.get_db_session.commit()
        await self._repo.get_db_session.refresh(new_product)

        return new_product

    async def update(self, id: int, update_model: ProductUpdate) -> Product | None:
        product = await self.get_one(id=id)

        if not product:
            raise get_404_exception()

        product_data = update_model.model_dump(exclude_unset=True)
        updated_product = await self._repo.update(id=product.id, data=product_data)

        await self._repo.get_db_session.commit()
        await self._repo.get_db_session.refresh(updated_product)

        return updated_product

    async def delete(self, id: int) -> bool:
        delete_result = await self._repo.delete(id)

        if not delete_result:
            raise get_404_exception()

        await self._repo.get_db_session.commit()
        return True