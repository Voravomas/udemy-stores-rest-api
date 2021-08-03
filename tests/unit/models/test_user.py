from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        test_user = UserModel("test", "test")
        self.assertEqual(test_user.username, "test", "Login is invalid")
        self.assertEqual(test_user.password, "test", "Password is invalid")
