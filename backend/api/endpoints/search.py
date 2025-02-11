from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import select

from backend.db.models import Item
from backend.db.session import SessionLocal

router = APIRouter(
    prefix="/search",
)


@router.get("/database/get/{item_query}/")
async def get_items(item_query: str) -> List[Item]:
    with SessionLocal() as session:
        session.execute(
            select(Item).where(Item.name == item_query)
        )

