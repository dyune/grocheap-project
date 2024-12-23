from contextlib import asynccontextmanager

import aiosqlite

DATABASE_URL = "sqlite+aiosqlite:///./grocery_items_data.db"


@asynccontextmanager
async def get_db():
    """
    Ensures database connection is open when needed and cleaned up
    automatically when the context is exited.
    Returns rows as dictionaries using aiosqlite.Row factory.
    """
    db = await aiosqlite.connect("grocery_items_data.db")
    db.row_factory = aiosqlite.Row  # Return rows as dictionaries
    try:
        yield db
    finally:
        await db.close()
