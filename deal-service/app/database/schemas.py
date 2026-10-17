from pydantic import BaseModel


class DealCreate(BaseModel):
    order_id: int
    user_id: int


class DealRead(BaseModel):
    order_id: int
    user_id: int

    is_completed: bool