from typing import List, Dict, Tuple, Sequence, Any
from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy import text, Row
from sqlmodel import select
from backend.db.models import Item
from backend.db.session import SessionLocal


SEARCH_ITEMS = text("""
    SELECT * FROM items 
    WHERE name ILIKE :query OR brand ILIKE :query
""")


router = APIRouter(
    prefix="/search",
)


@router.get("/items/query")
async def search_items(
        query: str = Query(..., min_length=1, description="Search term for name, brand, or description"),
):
    query_like = f"%{query}%"
    with SessionLocal() as session:
        result = session.execute(SEARCH_ITEMS, {"query": query_like})
        items = result.mappings().all()

    return {"query": query, "items": items}
