import aiosqlite

DATABASE_PATH = "grocery_items_data.db"

# SQL script to create the table with a price column
CREATE_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT,
    link TEXT NOT NULL,
    image_url TEXT,
    size TEXT,
    store TEXT NOT NULL,
    price REAL, -- Added price column
    UNIQUE(name, link)
);
"""

# SQL Queries
INSERT_ITEM = """
INSERT OR IGNORE INTO items (name, brand, link, image_url, size, store, price) 
VALUES (?, ?, ?, ?, ?, ?, ?)
"""
GET_ALL_ITEMS = "SELECT * FROM items"
GET_ITEM_BY_ID = "SELECT * FROM items WHERE id = ?"
UPDATE_ITEM = """
UPDATE items SET name = ?, brand = ?, link = ?, image_url = ?, size = ?, store = ?, price = ? 
WHERE id = ?
"""
DELETE_ITEM = "DELETE FROM items WHERE id = ?"

SEARCH_ITEMS = """
SELECT * FROM items
WHERE 
    name LIKE ? OR 
    brand LIKE ? OR 
    store LIKE ?
"""


async def initialize_db():
    """Initialize the database schema."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(CREATE_ITEMS_TABLE)
        await db.commit()


# Item Functions
async def create_item(name, brand, link, image_url=None, size=None, store=None, price=None):
    """Insert a new item with price."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            INSERT_ITEM, (name, brand, link, image_url, size, store, price)
        )
        await db.commit()
        return cursor.lastrowid


async def fetch_all_items():
    """Fetch all items."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(GET_ALL_ITEMS)
        rows = await cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "brand": row[2],
                "link": row[3],
                "image_url": row[4],
                "size": row[5],
                "store": row[6],
                "price": row[7],
            }
            for row in rows
        ]


async def fetch_item_by_id(item_id):
    """Fetch an item by ID."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(GET_ITEM_BY_ID, (item_id,))
        row = await cursor.fetchone()
        return {
            "id": row[0],
            "name": row[1],
            "brand": row[2],
            "link": row[3],
            "image_url": row[4],
            "size": row[5],
            "store": row[6],
            "price": row[7],
        } if row else None


async def update_item(item_id, name, brand, link, image_url, size, store, price):
    """Update an item."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            UPDATE_ITEM, (name, brand, link, image_url, size, store, price, item_id)
        )
        await db.commit()


async def delete_item(item_id):
    """Delete an item."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(DELETE_ITEM, (item_id,))
        await db.commit()


async def search_items(query: str):
    """Search for items by name, brand, or store."""
    query_like = f"%{query}%"  # Add wildcards for partial matching
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(SEARCH_ITEMS, (query_like, query_like, query_like))
        rows = await cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "brand": row[2],
                "link": row[3],
                "image_url": row[4],
                "size": row[5],
                "store": row[6],
                "price": row[7],
            }
            for row in rows
        ]


# Run to initialize the database
if __name__ == "__main__":
    import asyncio

    asyncio.run(initialize_db())
