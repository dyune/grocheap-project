from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import *

app = FastAPI()


# Initialize the database
@app.on_event("startup")
async def startup():
    await initialize_db()


# Add a new item
@app.post("/items/")
async def add_item(name: str, brand: str, category: str, keywords: str):
    item_id = await create_item(name, brand, category, keywords)
    return {"id": item_id, "name": name, "brand": brand, "category": category, "keywords": keywords}


# Fetch all items
@app.get("/items/")
async def get_items():
    items = await fetch_all_items()
    return items


# Fetch a specific item by ID
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = await fetch_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Edit an existing item
@app.put("/items/{item_id}")
async def edit_item(item_id: int, name: str, brand: str, category: str, keywords: str):
    await update_item(item_id, name, brand, category, keywords)
    return {"id": item_id, "name": name, "brand": brand, "category": category, "keywords": keywords}


# Delete an item
@app.delete("/items/{item_id}")
async def remove_item(item_id: int):
    await delete_item(item_id)
    return {"message": "Item deleted"}


@app.get("/prices/get/{item_id}")
async def get_prices(price_data: PriceGetRequest):
    item_prices = await fetch_prices_by_item(
        price_data.item_id,
        price_data.store_id
    )
    return item_prices


class PriceCreateRequest(BaseModel):
    item_id: int
    store_id: int
    price: float
    url: str | None = None


@app.post("/prices/post")
async def post_price(price_data: PriceCreateRequest):
    price_id = await create_price(
        price_data.item_id,
        price_data.store_id,
        price_data.price,
        price_data.url
    )
    return {
        "id": price_id,
        "item_id": price_data.item_id,
        "store_id": price_data.store_id,
        "price": price_data.price,
        "url": price_data.url
    }



