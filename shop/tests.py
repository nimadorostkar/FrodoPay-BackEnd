from django.test import TestCase



class ShopTests(TestCase):
    def test_shop_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
