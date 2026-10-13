from sqlmodel import SQLModel, Field, Relationship


class Order(SQLModel, table=True):
    __tablename__ = "orders" # type: ignore

    id: int | None = Field(primary_key=True, default=None)
    user_id: int

    products: list[ProductInOrder] = Relationship(back_populates="order", cascade_delete=True)


class ProductInOrder(SQLModel, table=True):
    __tablename__ = "products_in_order" # type: ignore

    id: int | None = Field(primary_key=True, default=None)

    product_id: int
    product_title: str
    product_description: str
    product_price: int = Field(gt=1.0, decimal_places=2)

    order_id: int = Field(foreign_key="orders.id")
    order: Order = Relationship(back_populates="products")