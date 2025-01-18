from typing import Optional, List

from sqlalchemy import insert

from backend.db.models import Item
from backend.db.session import Session, engine
from backend.schemas import items
from backend.schemas.items import ItemCreate

BATCH_SIZE = 100


async def save_product_to_db(name, brand, link, image_url, size, store, price) -> Optional[Item]:
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


def create_db_item(name, brand, link, image_url, size, store, price) -> Optional[Item]:
    try:
        item: ItemCreate = items.instantiate_item(name, brand, link, image_url, size, store, price)
        db_item: Item = Item(**item.model_dump())
        return db_item

    except Exception as e:
        print(f"Failed to save: {e}")
        return None


async def save_products_to_db(products: List[Optional[Item]]) -> List[Optional[Item]]:
    """
    Save a batch of products to the database.
    """
    saved_items = []

    for i in range(0, len(products), BATCH_SIZE):
        try:
            batch = products[i:i + BATCH_SIZE]
            dict_batch = []
            for item in batch:
                dict_batch.append(item.model_dump())

            with Session(engine) as session:  # Use a context manager to ensure proper cleanup
                query = insert(Item).values(dict_batch).prefix_with("OR REPLACE")
                session.execute(query)
                session.commit()

                # Refresh individual items in the batch if needed
                for item in batch:
                    saved_items.append(item)

        except Exception as e:
            print(f"Failed to save due to: {e}")

    return saved_items
