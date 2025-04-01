from typing import Optional, List
import re
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from backend.db.models import Item
from backend.db.session import SessionLocal
from backend.schemas import items
from backend.schemas.items import ItemCreate

BATCH_SIZE = 100


def save_product_to_db(name, brand, link, image_url, size, store_id, price) -> Optional[Item]:
    """
    Save a single product to the database.
    """
    try:
        item: ItemCreate = items.instantiate_item(name, brand, link, image_url, size, store_id, price)
        db_item: Item = Item(**item.model_dump())

        with SessionLocal() as session:
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            print(f"Saved: {db_item}")

        return db_item

    except SQLAlchemyError as e:
        print(f"Failed to save: {e}")
        return None


def create_db_item(name, brand, link, image_url, size, store_id, price) -> Optional[Item]:
    """
    Create an item instance without saving to the database.
    """
    try:
        item: ItemCreate = items.instantiate_item(name, brand, link, image_url, size, store_id, price)
        return Item(**item.model_dump())

    except SQLAlchemyError as e:
        print(f"Failed to create item: {e}")
        return None


def save_products_to_db(products: List[Optional[Item]]) -> List[Optional[Item]]:
    saved_items = []

    with SessionLocal() as session:
        for i in range(0, len(products), BATCH_SIZE):
            try:
                batch = products[i : i + BATCH_SIZE]
                batch = [item for item in batch if item]

                if not batch:
                    continue

                seen = set()
                dict_batch = []
                for item in batch:
                    key = (item.name, item.link, item.store_id)
                    if key not in seen:
                        seen.add(key)
                        dict_batch.append(item.model_dump(exclude={"id"}))

                query = insert(Item).values(dict_batch).on_conflict_do_nothing()
                session.execute(query)

                for item in batch:
                    session.query(Item).filter_by(
                        name=item.name, link=item.link, store_id=item.store_id
                    ).update({
                        "brand": item.brand,
                        "image_url": item.image_url,
                        "size": item.size,
                        "price": item.price
                    })

                session.commit()
                saved_items.extend(batch)

            except SQLAlchemyError as e:
                session.rollback()
                print(f"Failed to save batch due to: {e}")

    return saved_items


def parse_unit_price(text):
    match = re.search(r"\d+\s*/\s*\$\d+\.\d{2}", text)
    if match:
        quantity = int(match.group(1))
        total_price = float(match.group(2))
        unit_price = total_price / quantity
        return round(unit_price, 2)
    print("No match", text)
    return None


