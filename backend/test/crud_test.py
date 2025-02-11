import unittest
from backend.db.models import Item
from backend.services.scrapers.scrape_utils import save_product_to_db
from backend.db.session import SessionDep


class CrudTesting(unittest.IsolatedAsyncioTestCase):
    async def test_create_item_success(self):
        item: Item = Item(
            name='b',
            brand='b',
            link='a',
            image_url='a',
            size='12',
            store_id='1',
            price='12'
        )
        response = await save_product_to_db(item.name,
                                            item.brand,
                                            item.link,
                                            item.image_url,
                                            item.size,
                                            item.store_id,
                                            item.price,
                                            )
        self.assertEqual(item, response)  # add assertion here

    async def test_create_item_fail(self):
        item: Item = Item(
            name='a',
            brand='a',
            link='a',
            image_url='a',
            size=12,
            store_id=1,
            price="d"
        )
        print(item)
        response = await save_product_to_db(item.name,
                                            item.brand,
                                            item.link,
                                            item.image_url,
                                            item.size,
                                            item.store_id,
                                            item.price,
                                            )
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()


