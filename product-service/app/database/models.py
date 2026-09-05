from sqlmodel import SQLModel, Field, Relationship


class Product(SQLModel, table=True):
    """Модель товаров"""
    
    __tablename__ = "product"  # type: ignore
    id: int = Field(primary_key=True)

    title: str
    description: str
    photo_uri: str
    price: int = Field(decimal_places=2, gt=1.0)

    category_id: int | None = Field(default=None, foreign_key="categories.id")
    category: Category = Relationship(back_populates="products")


class Category(SQLModel, table=True):
    """Модель категорий к товарам"""

    __tablename__ = "categories" # type: ignore
    id: int = Field(primary_key=True)

    title: str
    comment: str

    products: list[Product] = Relationship(back_populates="category", cascade_delete=True)