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

# Define the path to the text file
TEXT_FILE_PATH = "input_data.txt"

# deniz wrote this
# Define the input model
# class InputText(BaseModel):
#     text: str
#

# @app.post("/write-text/")
# async def write_text(input_text: InputText):
#     try:
#         # Write the input text to the file
#         with open(TEXT_FILE_PATH, "a") as file:  # Use "a" to append
#             file.write(f"{input_text.text}\n")
#         return {"message": "Text written successfully!"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#


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


# Store Endpoints
@app.post("/stores/")
async def add_store(store: StoreCreateRequest):
    store_id = await create_store(store.name, store.website)
    return {"id": store_id, **store.dict()}


@app.get("/stores/", response_model=List[dict])
async def get_stores():
    stores = await fetch_all_stores()
    return stores


# Price Endpoints
@app.post("/prices/")
async def add_price(price: PriceCreateRequest):
    price_id = await create_price(price.store_id, price.item_id, price.price, price.url)
    return {"id": price_id, **price.dict()}


@app.get("/prices/{item_id}")
async def get_prices_for_item(item_id: int):
    prices = await fetch_prices_by_item(item_id)
    if not prices:
        raise HTTPException(status_code=404, detail="Prices not found for this item")
    return prices


@app.get("/prices/{item_id}/{store_id}")
async def get_latest_price(item_id: int, store_id: int):
    latest_price = await fetch_latest_price(item_id, store_id)
    if not latest_price:
        raise HTTPException(status_code=404, detail="No price found for this item in the specified store")
    return latest_price


@app.put("/prices/{price_id}")
async def edit_price(price_id: int, price: PriceUpdateRequest):
    await update_price(price_id, price.price, price.url)
    return {"id": price_id, **price.dict()}


@app.delete("/prices/{price_id}")
async def remove_price(price_id: int):
    await delete_price(price_id)
    return {"message": "Price deleted"}


# Search for items by name, brand, category, or keywords.
@app.get("/items/search/")
async def search_items_endpoint(query: str):
    items = await search_items(query)
    if not items:
        raise HTTPException(status_code=404, detail="No items found matching your search")
    return items
