from typing import Optional

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(max_length=255, min_length=1)
    brand: Optional[str] = Field(default=None, max_length=255, min_length=1)
    link: str = Field(default=None, max_length=400, min_length=1)
    image_url: Optional[str] = Field(default=None, max_length=400, min_length=1)
    size: str = Field(max_length=25, min_length=1)
    store_id: int
    price: float


class ItemUpdate(BaseModel):
    name: str = Field(max_length=255, min_length=1)
    brand: Optional[str] = Field(default=None, max_length=255, min_length=1)
    link: str = Field(default=None, max_length=400, min_length=1)
    image_url: Optional[str] = Field(default=None, max_length=400, min_length=1)
    size: str = Field(max_length=25, min_length=1)
    store_id: int
    price: float

    class Config:
        from_attributes = True


class ItemPublic(BaseModel):
    name: str
    name: str
    link: str
    image_url: str
    size: str
    store_id: int
    price: float

    class Config:
        from_attributes = True





