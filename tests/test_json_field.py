from django.test import TestCase
from .models import Order


class Test(TestCase):
    def test_json_crud(self):
        Order.objects.create(data={'amount': 10})
        self.assertEqual(Order.objects.first().data, {'amount': 10})
