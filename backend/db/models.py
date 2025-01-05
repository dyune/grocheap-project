from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint
from typing import Optional, List
from .associations import UserToItemAssociation


class Store(SQLModel, table=True):
    __tablename__ = "stores"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)

    inventory_items: List["Item"] = Relationship(back_populates="store")


class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    brand: Optional[str] = Field(max_length=100)
    link: str
    image_url: Optional[str]
    size: str = Field(max_length=50)
    store_id: int = Field(foreign_key="stores.id")
    price: float

    # Relationship to store the item belongs to
    store: "Store" = Relationship(back_populates="inventory_items")

    __table_args__ = UniqueConstraint("name",
                                      "link",
                                      "store_id",
                                      name="unique_name_link")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=100)
    email: str = Field(max_length=100)
    hashed_password: str = Field(max_length=100)

    # Unidirectional association: User * --> * Item
    saved_items: List["Item"] = Relationship(link_model=UserToItemAssociation)

    __table_args__ = UniqueConstraint("email", name="unique_email")
