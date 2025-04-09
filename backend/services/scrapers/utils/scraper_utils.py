from typing import Optional, List, Callable
import re

from bs4 import PageElement, ResultSet
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert
from backend.db.models import Item
from backend.db.session import SessionLocal
from backend.schemas import items
from backend.schemas.items import ItemCreate

BATCH_SIZE = 100


def prepare_urls(url_list) -> List[str]:
    res = []
    for url in url_list:
        res.extend(
            iterate_through_pages(url[0], url[1])
        )
    return res


def process_items_for_db(
        store_id: int,
        all_products: ResultSet,
        parse_product: Callable[[PageElement], dict]
) -> List[Item] | None:

    items_list = []

    try:
        for product in all_products:
            product_data = parse_product(product)

            if product_data["name"] and product_data["price"] and product_data["link"] is not None:
                db_item = create_db_item(
                    product_data["name"],
                    product_data["brand"],
                    product_data["link"],
                    product_data["image_url"],
                    product_data["size"],
                    store_id,
                    product_data["price"],
                )
                if db_item:
                    items_list.append(db_item)

            else:
                print(f"Product {product_data['name']} was missing essential information and could not be saved")

    except Exception as e:
        print(f"Failed to scrape: {e}")
        return None

    return items_list


#  -page-
#  ?page=
def iterate_through_pages(link: str, max_pages: int, pattern: str) -> List[str]:
    index = 1
    pages = []
    while index <= max_pages:
        if index == 1:
            pages.append(link)
        else:
            paginated_link = link + f"{pattern}{index}"
            pages.append(paginated_link)
        index += 1
    return pages


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
    """
    Batch save items to database.
    On INSERT conflict, will attempt to update with new data.
    """
    saved_items = []

    with SessionLocal() as session:
        for i in range(0, len(products), BATCH_SIZE):
            try:
                batch = products[i: i + BATCH_SIZE]
                batch = [item for item in batch if item]

                if not batch:
                    continue

                # Filter out duplicate entries
                seen = set()
                dict_batch = []
                for item in batch:
                    key = (item.name, item.link, item.store_id)
                    if key not in seen:
                        seen.add(key)
                        dict_batch.append(item.model_dump(exclude={"id"}))

                # Insert new items into the database
                query = insert(Item).values(dict_batch).on_conflict_do_nothing()
                session.execute(query)

                # Update new items brand, image, size, and/or price
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


def parse_unit_price(text) -> Optional[float]:
    match = re.search(r"\d+\s*/\s*\$\d+\.\d{2}", text)
    if match:
        quantity = int(match.group(1))
        total_price = float(match.group(2))
        unit_price = total_price / quantity
        return round(unit_price, 2)
    print("No match", text)
    return None
