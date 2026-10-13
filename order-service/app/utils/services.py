from typing import Sequence

from app.database.schemas import ProductInOrderAdd
from app.database.models import Order, ProductInOrder

from fastapi import HTTPException, status

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def create_new_order_for_user(
        user_id: int, 
        products: list[ProductInOrderAdd],
        db_session: AsyncSession) -> dict[str, str]:
    """Создание нового заказа для пользователя"""

    serialize_models = [ProductInOrder(**prod.model_dump()) for prod in products]
    new_order = Order(user_id=user_id, products=serialize_models)

    db_session.add(new_order)
    await db_session.commit()
    await db_session.refresh(new_order)

    return {"message": f"Создан новый заказ для пользователя {user_id}"}


async def get_all_orders_user(user_id: int, db_session: AsyncSession) -> Sequence[Order]:
    """Сервис, для получения всех заказов, которые имеются у пользователя"""
    statement = select(Order).where(Order.user_id == user_id).options(selectinload(Order.products)) # type: ignore
    
    query = await db_session.exec(statement)
    current_order = query.all()

    if not len(current_order):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не имеет заказов!")

    return current_order
