from fastapi import FastAPI, HTTPException, Body
from models import (
    initialize_db,
    create_item,
    fetch_all_items,
    fetch_item_by_id,
    update_item,
    delete_item,
)
from pydantic import BaseModel
import os

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

# Define the input model
class InputText(BaseModel):
    text: str

@app.post("/write-text/")
async def write_text(input_text: InputText):
    try:
        # Write the input text to the file
        with open(TEXT_FILE_PATH, "a") as file:  # Use "a" to append
            file.write(f"{input_text.text}\n")
        return {"message": "Text written successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialize the database
@app.on_event("startup")
async def startup():
    await initialize_db()


@app.post("/items/")
async def add_item(name: str, description: str, price: float):
    item_id = await create_item(name, description, price)
    return {"id": item_id, "name": name, "description": description, "price": price}


@app.get("/items/")
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
async def edit_item(item_id: int, name: str, description: str, price: float):
    await update_item(item_id, name, description, price)
    return {"id": item_id, "name": name, "description": description, "price": price}


@app.delete("/items/{item_id}")
async def remove_item(item_id: int):
    await delete_item(item_id)
    return {"message": "Item deleted"}
