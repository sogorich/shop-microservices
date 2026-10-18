from fastapi import APIRouter, Body, Depends, Path, Request
from typing import Annotated, Sequence

from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.database import get_session
from app.database.schemas import ProductInOrderAdd, OrderRead
from app.database.models import Order
from app.utils.services import create_new_order_for_user, get_all_orders_user


router = APIRouter(prefix="/api", tags=["Сервис заказов"])


@router.post("/orders")
async def create_order(
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_session)],
    payload_product_in_order: Annotated[list[ProductInOrderAdd], Body()]
) -> dict[str, str]:
    
    return await create_new_order_for_user(
        request,
        user_id=1, 
        products=payload_product_in_order, 
        db_session=db_session
    )


@router.get("/orders/{user_id}", response_model=Sequence[OrderRead])
async def get_order(
    user_id: Annotated[int, Path()],
    db_session: Annotated[AsyncSession, Depends(get_session)]) -> Sequence[Order]:

    return await get_all_orders_user(user_id, db_session)
