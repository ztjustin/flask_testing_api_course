from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class TestStore(BaseTest):
    # def test_create_store(self):
    #     with self.app_context():
    #         store = StoreModel('test')
    #         self.assertListEqual(store.items.all(), [], "The store items length was not 0")

    def test_Crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'))

    def test_Store_relation(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')

    def test_store_json(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name': 'test',
                'items': [{'name': 'test_item', 'price': 19.99}]
            }

            self.assertDictEqual(store.json(), expected)
