from sqlmodel import SQLModel


class OrderRead(SQLModel):
    products: list[ProductInOrderAdd]


class ProductInOrderAdd(SQLModel):
    product_id: int
    product_title: str
    product_description: str
    product_price: int
