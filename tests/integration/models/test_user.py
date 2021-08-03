from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test', 'abcd')
            self.assertIsNone(UserModel.find_by_username(user.username))
            self.assertIsNone(UserModel.find_by_id(user.id))

            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_username(user.username))
            self.assertIsNotNone(UserModel.find_by_id(user.id))

