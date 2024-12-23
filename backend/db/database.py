from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from enum import Enum
from .models import Item
from .session import get_session

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/database"
)


def save(item, session: SessionDep):
    session.add(item)
    session.commit()
    session.refresh(item)


# GET ENDPOINTS
@router.get("/item/{id}")
async def get_item_by_id(identifier: int, session: SessionDep):
    item = session.exec(select(Item).where(Item.id == identifier))
    return item


@router.get("/items") # TODO: For testing purposes
async def get_items(session: SessionDep):
    items = session.exec(select(Item)).all()
    return items


@router.get("/item/filter")
async def get_item_filter(item_id: int, session: SessionDep):
    pass


# POST METHODS
@router.post("create/item")
async def create_item(item: Item, session: SessionDep):
    try:
        save(item, session)
        return item

    except Exception as e:
        return None


@router.put("/item/{id}")
async def update_item_price(identifier: int, session: SessionDep, price: float):
    item = get_item_by_id(identifier, session)
    if item is None:
        return None
    else:
        item.price = price
        save(item, session)
        return item





