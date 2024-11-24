from typing import Optional, List

from fastapi import FastAPI, HTTPException, Body
from models import *
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.on_event("startup")
async def startup():
    """Initialize the database when the app starts."""
    await initialize_db()


# Pydantic Models for Request Validation
class ItemCreateRequest(BaseModel):
    name: str
    brand: Optional[str]
    category: Optional[str]
    keywords: Optional[str]


class StoreCreateRequest(BaseModel):
    name: str
    website: str


class PriceCreateRequest(BaseModel):
    store_id: int
    item_id: int
    price: float
    url: Optional[str]


class PriceUpdateRequest(BaseModel):
    price: float
    url: Optional[str]


# Item Endpoints
@app.post("/items/")
async def add_item(item: ItemCreateRequest):
    item_id = await create_item(item.name, item.brand, item.category, item.keywords)
    return {"id": item_id, **item.dict()}


@app.get("/items/", response_model=List[dict])
async def get_items():
    items = await fetch_all_items()
    return items


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = await fetch_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}")
async def edit_item(item_id: int, item: ItemCreateRequest):
    await update_item(item_id, item.name, item.brand, item.category, item.keywords)
    return {"id": item_id, **item.dict()}


@app.delete("/items/{item_id}")
async def remove_item(item_id: int):
    await delete_item(item_id)
    return {"message": "Item deleted"}


# Search for items by name, brand, category, or keywords.
@app.get("/items/search/")
async def search_items_endpoint(query: str):
    items = await search_items(query)
    if not items:
        raise HTTPException(status_code=404, detail="No items found matching your search")
    return items
