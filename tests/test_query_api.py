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

    def test_contains_query(self):
        person = Person.objects.get(name__icontains='John')
        self.assertEqual(person.name, 'John Doe')

    def test_isnull_query(self):
        persons = Person.objects.filter(name__isnull=True)
        self.assertEqual(0, persons.count())
        persons = Person.objects.filter(name__isnull=False)
        self.assertEqual(2, persons.count())
