from django.test import TestCase
from .models import Order, Person


class Test(TestCase):
    def test_json_crud(self):
        Order.objects.create(data={'amount': 10})
        self.assertEqual(Order.objects.first().data, {'amount': 10})

    def test_json_tore_crud(self):
        Person.objects.create(data={'name': 'John'})
        self.assertEqual(Person.objects.first().data, {'name': 'John'})
