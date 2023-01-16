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

    def test_values_list(self):
        Person.objects.create(name='john')
        query = Person.objects.values_list('name')
        self.assertEqual(list(query), [('john',)])
