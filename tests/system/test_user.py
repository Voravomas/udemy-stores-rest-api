from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response_register = client.post("/register",
                                                data={'username': 'test',
                                                      'password': 'abcd'})
                self.assertEqual(response_register.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'Success: User created successfully'},
                                     json.loads(response_register.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={'username': 'test',
                                               'password': 'abcd'})
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test',
                                                            'password': 'abcd'}),
                                           headers={'Content-type': 'application/json'})
                self.assertIn('access_token', json.loads(auth_request.data).keys())

    def test_register_duplication_error(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={'username': 'test',
                                               'password': 'abcd'})
                again_register_responce = client.post("/register", data={'username': 'test',
                                                                         'password': 'abcd'})
                self.assertEqual(again_register_responce.status_code, 400)
                self.assertDictEqual(json.loads(again_register_responce.data),
                                     {'message': "Error: Already exists"})
