from typing import Optional
from pydantic import BaseModel, Field

# DTO classes


class ItemCreate(BaseModel):
    name: str = Field(max_length=255, min_length=1)
    brand: Optional[str] = Field(max_length=255, min_length=1)
    link: str = Field(max_length=400, min_length=1)
    image_url: Optional[str] = Field(max_length=400, min_length=1)
    size: str = Field(max_length=50, min_length=1)
    store_id: int
    price: float


class ItemUpdate(BaseModel):
    name: str = Field(max_length=255, min_length=1)
    brand: Optional[str] = Field(max_length=255, min_length=1)
    link: str = Field(max_length=400, min_length=1)
    image_url: Optional[str] = Field(max_length=400, min_length=1)
    size: str = Field(max_length=25, min_length=1)
    store_id: int
    price: float

    class Config:
        from_attributes = True


def instantiate_item(
        name: str,
        brand: Optional[str],
        link: str,
        image_url: Optional[str],
        size: str,
        store_id: int,
        price: float
) -> Optional[ItemCreate]:

    try:
        return ItemCreate(
            name=name,
            brand=brand,
            link=link,
            image_url=image_url,
            size=size,
            store_id=store_id,
            price=price
        )

    except ValueError as e:
        print(f"Validation error: {e}")
        return None



