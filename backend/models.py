import aiosqlite

from database import get_db

# Define all SQL queries
CREATE_ITEMS_TABLE = """
create table if not exists items
(
    id       INTEGER primary key autoincrement,
    name     TEXT not null,
    brand    TEXT,
    category TEXT,
    unique (name, brand)
);
"""
CREATE_PRICES_TABLE = """
create table if not exists prices
(
    id       INTEGER primary key autoincrement,
    store_id INTEGER not null references stores,
    item_id  INTEGER not null references items,
    price    REAL    not null,
    url      TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
CREATE_STORES_TABLE = """
create table if not exists stores
(
    id      INTEGER PRIMARY KEY autoincrement,
    name    TEXT NOT NULL UNIQUE,
    website TEXT NOT NULL
);
"""

INSERT_STORE = "INSERT INTO stores (name, website) VALUES (?, ?)"
GET_ALL_STORES = "SELECT * FROM stores"
GET_STORE_BY_ID = "SELECT * FROM stores WHERE id = ?"
UPDATE_STORE = "UPDATE stores SET name = ?, website = ? WHERE id = ?"
DELETE_STORE = "DELETE FROM stores WHERE id = ?"

INSERT_PRICE = """
INSERT INTO prices (store_id, item_id, price, url) 
VALUES (?, ?, ?, ?)
"""
GET_PRICES_BY_ITEM = """
SELECT p.id, s.name AS store_name, p.price, p.url, p.last_updated 
FROM prices p
JOIN stores s ON p.store_id = s.id
WHERE p.item_id = ?
"""
GET_LATEST_PRICE = """
SELECT p.id, p.price, p.url, p.last_updated 
FROM prices p
WHERE p.item_id = ? AND p.store_id = ?
ORDER BY p.last_updated DESC
LIMIT 1
"""
DELETE_PRICE = "DELETE FROM prices WHERE id = ?"


INSERT_ITEM = "INSERT INTO items (name, description, price) VALUES (?, ?, ?)"
GET_ALL_ITEMS = "SELECT * FROM items"
GET_ITEM_BY_ID = "SELECT * FROM items WHERE id = ?"
UPDATE_ITEM = "UPDATE items SET name = ?, description = ?, price = ? WHERE id = ?"
DELETE_ITEM = "DELETE FROM items WHERE id = ?"

DATABASE_PATH = "grocery_items_data.db"


async def initialize_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Initialize the database schema
        await db.execute(CREATE_ITEMS_TABLE)
        await db.commit()
        await db.execute(CREATE_STORES_TABLE)
        await db.commit()
        await db.execute(CREATE_PRICES_TABLE)
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
