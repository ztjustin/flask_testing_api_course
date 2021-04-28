from models.item import ItemModel
from tests.base_test import BaseTest
from models.user import UserModel
from models.store import StoreModel
import json


class TestItem(BaseTest):

    def setUp(self):
        super(TestItem, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth', data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})

                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = 'JWT ' + auth_token

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'could not authorize'}, json.loads(resp.data))

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_Get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.delete('/item/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(resp.data))

    def test_create_duplicated_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()

                resp = client.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "An item with name '{}' already exists.".format('test')},
                                     json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.put('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 5.99)

                resp = client.put('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                resp = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 5.99}]}, json.loads(resp.data))
