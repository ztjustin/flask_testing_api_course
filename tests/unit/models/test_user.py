from tests.unit.unit_base_Test import UnitBasetest
from models.user import UserModel


class TestUser(UnitBasetest):
    def test_create_user(self):
        user = UserModel('test', 'abcd')

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, 'abcd')
