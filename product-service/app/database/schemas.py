from sqlmodel import SQLModel, Field
from .models import Category


class ProductRead(SQLModel):
    """Схема для отображения данных о товаре"""
    id: int

    title: str
    description: str
    photo_uri: str
    price: int

    category: Category | None = Field(default=None)


class ProductCreate(SQLModel):
    """Cхема, используемая при создании товара"""
    title: str
    description: str
    photo_uri: str
    price: int


class ProductUpdate(SQLModel):
    """Cхема, используемая при обновления данных товара"""
    title: str | None = None
    description: str | None = None
    photo_uri: str | None = None
    price: int | None = None