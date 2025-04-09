from datetime import datetime
from typing import Optional, List

from sqlalchemy import (
    UniqueConstraint,
    ForeignKey,
    Integer,
    String,
    Float,
    DateTime,
)
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

Base = declarative_base()


class Store(Base):
    __tablename__ = "stores"
    __table_args__ = (UniqueConstraint("name", name="unique_store_name"),)

    id:   Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationship: One store has many items, enables Store -> Item traversal
    inventory_items: Mapped[List["Item"]] = relationship("Item", back_populates="store")


class Item(Base):
    __tablename__ = "items"
    __table_args__ = (UniqueConstraint("name", "link", "store_id", name="unique_name_link"),)

    id:        Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False)
    name:      Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    brand:     Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    link:      Mapped[str] = mapped_column(String(300), nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    size:      Mapped[str] = mapped_column(String(50), nullable=False)
    store_id:  Mapped[int] = mapped_column(Integer, ForeignKey("stores.id"), nullable=False)
    price:     Mapped[float] = mapped_column(Float, nullable=False)

    # Relationship: Each item belongs to one store, enables Item -> Store traversal
    store:         Mapped["Store"] = relationship("Store", back_populates="inventory_items")
    price_history: Mapped[List["ItemPriceHistory"]] = relationship("ItemPriceHistory", back_populates="item")

    def equals(self, other: "Item") -> bool:
        return (
                self.name == other.name and
                self.brand == other.brand and
                self.link == other.link and
                self.image_url == other.image_url and
                self.size == other.size and
                self.store_id == other.store_id and
                self.price == other.price
        )


class ItemPriceHistory(Base):
    __tablename__ = "item_price_history"
    __table_args__ = (UniqueConstraint("item_id", "timestamp", name="unique_item_timestamp"),)

    id:        Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False)
    item_id:   Mapped[int] = mapped_column(Integer, ForeignKey("items.id"), nullable=False)
    price:     Mapped[float] = mapped_column(Float, nullable=False)
    datetime:  Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship: One to Many, one item has many price histories
    item: Mapped["Item"] = relationship("Item", back_populates="price_history")
