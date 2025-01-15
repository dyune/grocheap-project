from backend.db import crud
from backend.db.models import Item
from backend.schemas import items
from backend.db.session import Session, engine
from backend.schemas.items import ItemCreate
import tracemalloc


async def save_product_to_db(name, brand, link, image_url, size, store, price):
    try:
        item: ItemCreate = items.instantiate_item(name, brand, link, image_url, size, store, price)
        db_item: Item = Item(**item.model_dump())
        print(db_item)
        session = Session(engine)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        print(f"Saved: {item}")
        return db_item

    except Exception as e:
        print(f"Failed to save: {e}")
        return None

