from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint
from typing import Optional, List


class Store(SQLModel, table=True):
    __tablename__ = "stores"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    items: List["Item"] = Relationship(back_populates="store")


class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    brand: Optional[str] = Field(max_length=100)
    link: str = Field(max_length=255)
    image_url: Optional[str] = Field(max_length=255)
    size: str = Field(max_length=50)
    store_id: int = Field(foreign_key="stores.id")
    store: "Store" = Relationship(back_populates="items")
    price: float

    __table_args__ = (UniqueConstraint("name", "link", name="unique_name_link"),)



