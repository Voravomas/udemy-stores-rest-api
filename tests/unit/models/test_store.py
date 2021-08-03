from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_create_store(self):
        test_store = StoreModel("test_store")

        self.assertEqual(test_store.name, "test_store",
                         "Store name is incorrect")
