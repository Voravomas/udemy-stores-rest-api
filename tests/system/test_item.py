import json

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def setUp(self):
        super().setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'test',
                                                             'password': '1234'}),
                                            headers={'Content-type': 'application/json'})
                auth_token = json.loads(auth_response.data)['access_token']
                self.auth_header = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/item/piano")
                self.assertEqual(resp.status_code, 401)
                self.assertDictEqual(json.loads(resp.data),
                                     {'message': 'Error: Unable to authorize.' +
                                                 ' Please include valid authorization header'})

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test',
                                  headers={'Authorization': self.auth_header})
                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual(json.loads(resp.data),
                                     {'message': 'Item not found'})

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('PiaNo', 1000, 1).save_to_db()
                resp = client.get('/item/PiaNo',
                                  headers={'Authorization': self.auth_header})
                self.assertEqual(resp.status_code, 200, json.loads(resp.data))
                self.assertDictEqual(json.loads(resp.data),
                                     {'name': 'PiaNo', 'price': 1000})

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('PiaNo', 1000, 1).save_to_db()
                resp = client.delete('/item/PiaNo',
                                     headers={'Authorization': self.auth_header})

                self.assertEqual(resp.status_code, 200, json.loads(resp.data))
                self.assertDictEqual(json.loads(resp.data),
                                     {'message': 'Item deleted'})

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('big_store').save_to_db()
                resp = client.post('/item/PiaNo', data={'price': 1000, 'store_id': 1})
                self.assertEqual(resp.status_code, 201, json.loads(resp.data))
                self.assertDictEqual(json.loads(resp.data),
                                     {'name': 'PiaNo', 'price': 1000.0})

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('big_store').save_to_db()
                client.post('/item/PiaNo', data={'price': 1000, 'store_id': 1})
                resp = client.post('/item/PiaNo', data={'price': 1000, 'store_id': 1})
                self.assertEqual(resp.status_code, 400, json.loads(resp.data))
                self.assertDictEqual(json.loads(resp.data),
                                     {'message': "An item with name 'PiaNo' already exists."})

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('big_store').save_to_db()
                resp = client.put('/item/PiaNo', data={'price': 1000, 'store_id': 1})
                self.assertEqual(resp.status_code, 200, json.loads(resp.data))
                self.assertDictEqual(json.loads(resp.data),
                                     {'name': 'PiaNo', 'price': 1000})

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('big_store').save_to_db()
                client.post('/item/PiaNo', data={'price': 1000, 'store_id': 1})
                resp = client.put('/item/PiaNo', data={'price': 500, 'store_id': 1})
                self.assertEqual(resp.status_code, 200, json.loads(resp.data))
                self.assertDictEqual(json.loads(resp.data),
                                     {'name': 'PiaNo', 'price': 500})

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('big_store').save_to_db()
                client.post('/item/PiaNo', data={'price': 1000, 'store_id': 1})
                client.post('/item/chair', data={'price': 50, 'store_id': 1})
                client.post('/item/table', data={'price': 100, 'store_id': 1})
                resp = client.get('/items')
                self.assertDictEqual(json.loads(resp.data),
                                     {'items': [
                                         {'name': 'PiaNo', 'price': 1000},
                                         {'name': 'chair', 'price': 50},
                                         {'name': 'table', 'price': 100}
                                     ]})
