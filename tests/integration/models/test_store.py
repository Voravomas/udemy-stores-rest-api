from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_items_empty(self):
        test_store = StoreModel("test_store")

        self.assertListEqual(test_store.items.all(), [],
                             "New store items list is not empty")

    def test_crud(self):
        with self.app_context():
            test_store = StoreModel("test_store")
            self.assertIsNone(StoreModel.find_by_name("test_store"),
                              "test_store already existed in db")

            test_store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name("test_store"),
                                 "test_store was not found in db")

            test_store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name("test_store"),
                              "test_store was not deleted from db")

    def test_store_relationship(self):
        with self.app_context():
            test_store = StoreModel("test_store")
            test_item = ItemModel("test", 0.0, 1)

            test_store.save_to_db()
            test_item.save_to_db()

            self.assertEqual(test_store.items.count(), 1)
            self.assertEqual(test_store.items[0].name, 'test')

    def test_store_json_empty(self):
        with self.app_context():
            test_store = StoreModel("test_store")

            test_store.save_to_db()

            expected = {'id': 1, 'name': "test_store", 'items': []}
            self.assertEqual(test_store.json(), expected)

    def test_store_json_one(self):
        with self.app_context():
            test_store = StoreModel("test_store")
            test_item = ItemModel("test", 0.0, 1)

            test_store.save_to_db()
            test_item.save_to_db()

            expected = {'id': 1, 'name': "test_store", 'items': [{'name': "test", 'price': 0.0}]}
            self.assertEqual(test_store.json(), expected)

    def test_store_json_many(self):
        with self.app_context():
            test_store = StoreModel("test_store")
            test_item1 = ItemModel("test", 0.0, 1)
            test_item2 = ItemModel("piano", 1000.0, 1)

            test_store.save_to_db()
            test_item1.save_to_db()
            test_item2.save_to_db()

            expected = {'id': 1,
                        'name': "test_store",
                        'items': [
                            {'name': "test", 'price': 0.0},
                            {'name': "piano", 'price': 1000.0},
                        ]
                        }
            self.assertEqual(test_store.json(), expected)


