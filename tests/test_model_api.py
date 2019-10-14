from django.test import TestCase

from .models import Person


class Test(TestCase):
    def test_person_crud(self):
        person = Person(name='John Doe')
        self.assertEqual(person.name, 'John Doe')
        self.assertEqual(person.data, {'name': 'John Doe'})

        person.save()
        person.refresh_from_db()

        self.assertEqual(person.name, 'John Doe')
        self.assertEqual(person.data, {'name': 'John Doe'})
