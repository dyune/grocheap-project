import aiosqlite

DATABASE_PATH = "grocery_items_data.db"

# SQL scripts to create tables
CREATE_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT,
    category TEXT,
    keywords TEXT,
    UNIQUE(name, brand)
);
"""

CREATE_PRICES_TABLE = """
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER NOT NULL REFERENCES stores(id),
    item_id INTEGER NOT NULL REFERENCES items(id),
    price REAL NOT NULL,
    url TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_STORES_TABLE = """
CREATE TABLE IF NOT EXISTS stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    website TEXT NOT NULL
);
"""

# SQL Queries
INSERT_ITEM = "INSERT INTO items (name, brand, category, keywords) VALUES (?, ?, ?, ?)"
GET_ALL_ITEMS = "SELECT * FROM items"
GET_ITEM_BY_ID = "SELECT * FROM items WHERE id = ?"
UPDATE_ITEM = "UPDATE items SET name = ?, brand = ?, category = ?, keywords = ? WHERE id = ?"
DELETE_ITEM = "DELETE FROM items WHERE id = ?"

INSERT_STORE = "INSERT INTO stores (name, website) VALUES (?, ?)"
GET_ALL_STORES = "SELECT * FROM stores"
GET_STORE_BY_ID = "SELECT * FROM stores WHERE id = ?"
UPDATE_STORE = "UPDATE stores SET name = ?, website = ? WHERE id = ?"
DELETE_STORE = "DELETE FROM stores WHERE id = ?"

INSERT_PRICE = "INSERT INTO prices (store_id, item_id, price, url) VALUES (?, ?, ?, ?)"
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
UPDATE_PRICE = """
UPDATE prices 
SET price = ?, url = ?, last_updated = CURRENT_TIMESTAMP 
WHERE id = ?
"""
DELETE_PRICE = "DELETE FROM prices WHERE id = ?"


async def initialize_db():
    """Initialize database schema."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(CREATE_ITEMS_TABLE)
        await db.execute(CREATE_STORES_TABLE)
        await db.execute(CREATE_PRICES_TABLE)
        await db.commit()


# Item Functions
async def create_item(name, brand, category, keywords):
    """Insert a new item."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(INSERT_ITEM, (name, brand, category, keywords))
        await db.commit()
        return cursor.lastrowid


async def fetch_all_items():
    """Fetch all items."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(GET_ALL_ITEMS)
        rows = await cursor.fetchall()
        return [{"id": row[0], "name": row[1], "brand": row[2], "category": row[3], "keywords": row[4]} for row in rows]


async def fetch_item_by_id(item_id):
    """Fetch an item by ID."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(GET_ITEM_BY_ID, (item_id,))
        row = await cursor.fetchone()
        return {"id": row[0], "name": row[1], "brand": row[2], "category": row[3], "keywords": row[4]} if row else None


async def update_item(item_id, name, brand, category, keywords):
    """Update an item."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(UPDATE_ITEM, (name, brand, category, keywords, item_id))
        await db.commit()


async def delete_item(item_id):
    """Delete an item."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(DELETE_ITEM, (item_id,))
        await db.commit()


# Store Functions
async def create_store(name, website):
    """Insert a new store."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(INSERT_STORE, (name, website))
        await db.commit()
        return cursor.lastrowid


async def fetch_all_stores():
    """Fetch all stores."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(GET_ALL_STORES)
        rows = await cursor.fetchall()
        return [{"id": row[0], "name": row[1], "website": row[2]} for row in rows]


# Price Functions
async def create_price(store_id, item_id, price, url=None):
    """Insert a new price."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(INSERT_PRICE, (store_id, item_id, price, url))
        await db.commit()
        return cursor.lastrowid


async def fetch_prices_by_item(item_id):
    """Fetch all prices for a specific item."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(GET_PRICES_BY_ITEM, (item_id,))
        rows = await cursor.fetchall()
        return [{"id": row[0], "store_name": row[1], "price": row[2], "url": row[3], "last_updated": row[4]} for row in rows]


async def fetch_latest_price(item_id, store_id):
    """Fetch the latest price for an item in a store."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(GET_LATEST_PRICE, (item_id, store_id))
        row = await cursor.fetchone()
        return {"id": row[0], "price": row[1], "url": row[2], "last_updated": row[3]} if row else None


async def update_price(price_id, price, url):
    """Update a price."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(UPDATE_PRICE, (price, url, price_id))
        await db.commit()


async def delete_price(price_id):
    """Delete a price."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(DELETE_PRICE, (price_id,))
        await db.commit()
