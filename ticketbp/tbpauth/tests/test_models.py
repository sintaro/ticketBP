from django.test import TestCase

from tbpauth.testing import factory_user


class TestUser(TestCase):
    def test_get_full_name(self):
        user = factory_user(last_name='田中', first_name='太郎')
        self.assertEqual(user.get_full_name(), '田中 太郎')

    def test_address(self):
        user = factory_user(address1='東京都練馬区', address2='ネリマーマンション')
        self.assertEqual(user.address(), '東京都練馬区 ネリマーマンション')
