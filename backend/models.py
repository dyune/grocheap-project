import aiosqlite

from database import get_db

CREATE_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL
);
"""

INSERT_ITEM = "INSERT INTO items (name, description, price) VALUES (?, ?, ?)"
GET_ALL_ITEMS = "SELECT * FROM items"
GET_ITEM_BY_ID = "SELECT * FROM items WHERE id = ?"
UPDATE_ITEM = "UPDATE items SET name = ?, description = ?, price = ? WHERE id = ?"
DELETE_ITEM = "DELETE FROM items WHERE id = ?"

DATABASE_PATH = "./test.db"


async def initialize_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Initialize the database schema
        await db.execute(CREATE_ITEMS_TABLE)
        await db.commit()


async def create_item(name, description, price):
    async with get_db() as db:
        cursor = await db.execute(INSERT_ITEM, (name, description, price))
        await db.commit()
        return cursor.lastrowid


async def fetch_all_items():
    async with get_db() as db:
        cursor = await db.execute(GET_ALL_ITEMS)
        return await cursor.fetchall()


async def fetch_item_by_id(item_id):
    async with get_db() as db:
        cursor = await db.execute(GET_ITEM_BY_ID, (item_id,))
        return await cursor.fetchone()


async def update_item(item_id, name, description, price):
    async with get_db() as db:
        await db.execute(UPDATE_ITEM, (name, description, price, item_id))
        await db.commit()


async def delete_item(item_id):
    async with get_db() as db:
        await db.execute(DELETE_ITEM, (item_id,))
        await db.commit()
