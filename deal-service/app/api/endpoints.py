from typing import Annotated
from fastapi import APIRouter, Query, Body

from app.database.schemas import DealCreate, DealRead
from app.database.models import Deal
from app.utils.services import create_new_deal, get_all_deals


router = APIRouter(prefix="/api", tags=["Работа со сделками"])


@router.post("/deals")
async def create_deal(body: Annotated[DealCreate, Body()]) -> str:
    return await create_new_deal(body.model_dump())


@router.get("/deals", response_model=list[DealRead])
async def get_active_deals(limit: Annotated[int, Query()] = 10) -> list[Deal]:
    return await get_all_deals(limit)