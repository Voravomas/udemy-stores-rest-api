import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/store/test_store')
                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))
                self.assertDictEqual(json.loads(resp.data), {'name': "test_store",
                                                             'items': []})

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                resp2 = client.post('/store/test_store')
                self.assertEqual(resp2.status_code, 400)
                self.assertDictEqual(json.loads(resp2.data),
                                     {'message': "A store with name 'test_store' already exists."})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))

                resp = client.delete('/store/test_store')
                self.assertEqual(resp.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name("test_store"))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                resp = client.get('store/test_store')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'items': [], 'name': 'test_store'})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('store/test_store')
                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Store not found'})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/test_store')
                item1 = ItemModel("piano2", 1000, 1)
                item2 = ItemModel("piano1", 1000, 1)
                item1.save_to_db()
                item2.save_to_db()
                resp = client.get('store/test_store')
                self.assertEqual(resp.status_code, 200, resp.data)
                self.assertDictEqual(json.loads(resp.data), {'items': [
                    {'name': "piano2", 'price': 1000},
                    {'name': "piano1", 'price': 1000},
                ], 'name': 'test_store'})

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store1')
                client.post('/store/test_store2')
                resp = client.get('/stores')
                self.assertDictEqual(json.loads(resp.data),
                                     {'stores': [
                                         {'items': [], 'name': 'test_store1'},
                                         {'items': [], 'name': 'test_store2'}
                                     ]})

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store1')
                client.post('/store/test_store2')
                ItemModel("piano1", 1000, 1).save_to_db()
                ItemModel("piano2", 1000, 2).save_to_db()

                resp = client.get('/stores')
                self.assertDictEqual(json.loads(resp.data),
                                     {'stores': [
                                         {'items': [
                                             {'name': "piano1", 'price': 1000},
                                         ], 'name': 'test_store1'},
                                         {'items': [
                                             {'name': "piano2", 'price': 1000},
                                         ], 'name': 'test_store2'}
                                     ]})
