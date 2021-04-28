from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class TestStore(BaseTest):
    def test_find_store(self):
        with self.app() as client:
            with self.app_context():  # to get all the method of the database
                StoreModel('test').save_to_db()
                req = client.get('/store/test')

                self.assertEqual(req.status_code, 200)
                self.assertDictEqual({'name': 'test', 'items': []}, json.loads(req.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():  # to get all the method of the database
                client.post('/store/test')
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "A store with name '{}' already exists.".format('test')},
                                     json.loads(response.data))

    def test_create_store(self):
        with self.app() as client:
            with self.app_context():  # to get all the method of the database
                req = client.post('/store/test')

                self.assertEqual(req.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'name': 'test', 'items': []}, json.loads(req.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():  # to get all the method of the database
                StoreModel('test').save_to_db()
                req = client.delete('/store/test')

                self.assertEqual(req.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(req.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():  # to get all the method of the database
                req = client.get('/store/test')

                self.assertEqual(req.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(req.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():  # to get all the method of the database
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                req = client.get('/store/test')

                self.assertEqual(req.status_code, 200)
                self.assertDictEqual({'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]},
                                     json.loads(req.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():  # to get all the method of the database
                StoreModel('test').save_to_db()

                req = client.get('/stores')

                self.assertEqual(req.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'test', 'items': []}]}, json.loads(req.data))

    def test_store_with_items(self):
        with self.app() as client:
            with self.app_context():  # to get all the method of the database
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                req = client.get('/stores')

                self.assertEqual(req.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]}]},
                                     json.loads(req.data))
