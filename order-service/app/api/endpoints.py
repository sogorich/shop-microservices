from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Annotated

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.database import get_session
from app.database.schemas import OrderCreate, ProductInOrderAdd, OrderRead
from app.database.models import Order, ProductInOrder


router = APIRouter(prefix="/api", tags=["Сервис заказов"])


@router.post("/orders")
async def create_order(
    db_session: Annotated[AsyncSession, Depends(get_session)],
    payload_product_in_order: Annotated[ProductInOrderAdd, Body()]
):
    order_scheme = OrderCreate(user_id=1)
    statement = select(Order).where(Order.user_id == order_scheme.user_id)
    query = await db_session.exec(statement)

    current_order = query.first()

    if not current_order:
        new_order = Order(**order_scheme.model_dump())
        db_session.add(new_order)
        await db_session.commit()
        await db_session.refresh(new_order)

        product = ProductInOrder(order_id=new_order.id, **payload_product_in_order.model_dump())
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)

    if current_order:
        product = ProductInOrder(order_id=current_order.id, **payload_product_in_order.model_dump())
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)

    return {"message": f"Продукт {payload_product_in_order.product_title} добавлен в заказ пользователю {order_scheme.user_id}"}


@router.get("/orders", response_model=OrderRead)
async def get_order(db_session: Annotated[AsyncSession, Depends(get_session)]) -> Order:
    fake_user_id = 1

    statement = select(Order).where(Order.user_id == fake_user_id).options(selectinload(Order.products)) # type: ignore
    
    query = await db_session.exec(statement)
    current_order = query.first()

    if not current_order:
        raise HTTPException(404, "Пользователь не имеет заказов!")

    return current_order
