import unittest
from backend.db.models import Item
from backend.schemas.items import instantiate_item


class ModelsTesting(unittest.TestCase):
    def test_equals_method(self):
        item_1_data = instantiate_item('a', 'a', 'a', 'a', '10', 1, 12)
        item_2_data = instantiate_item('a', 'a', 'a', 'a', '10', 1, 12)

        item_1: Item = Item(
            name=item_1_data.name,
            brand=item_1_data.brand,
            link=item_1_data.link,
            image_url=item_1_data.image_url,
            size=item_1_data.size,
            store_id=item_1_data.store_id,
            price=item_1_data.price
        )
        item_2: Item = Item(
            name=item_2_data.name,
            brand=item_2_data.brand,
            link=item_2_data.link,
            image_url=item_2_data.image_url,
            size=item_2_data.size,
            store_id=item_2_data.store_id,
            price=item_2_data.price
        )

        self.assertTrue(item_1.equals(item_2), "Item equality should have been equal.")


if __name__ == '__main__':
    unittest.main()
