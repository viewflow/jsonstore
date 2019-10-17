from unittest import skipUnless
from django.db import connection
from django.test import TestCase
from .models import Person


@skipUnless(
    connection.vendor in ['postgresql', 'mysql', 'oracle'],
    "Databases with first-class JSONField support"
)
class Test(TestCase):
    def setUp(self):
        Person.objects.create(name='John Doe')
        Person.objects.create(name='Will Smith')

    def test_iexact_query(self):
        person = Person.objects.get(name='John Doe')
        self.assertEqual(person.name, 'John Doe')
