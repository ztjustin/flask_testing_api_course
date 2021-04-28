from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_Register_user(self):
        with self.app() as client:
            with self.app_context():  # to get all the method of the database
                req = client.post('/register', data={'username': 'test', 'password': '1234'})
                self.assertEqual(req.status_code, 201)

                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({"message": "User created successfully"}, json.loads(req.data))

    def test_register_login_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                auth_request = client.post('/auth', data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                self.assertIn('access_token', json.loads(auth_request.data).keys())

    def test_register_duplicated(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'},
                                     json.loads(response.data))
