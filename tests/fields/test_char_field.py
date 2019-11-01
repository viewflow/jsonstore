from django.db import models
from django.test import TestCase
from jsonfield_schema import JSONField, JSONSchema


class Schema(JSONSchema):
    char_field = {
        'type': "string",
        'maxLength': 250,
    }

    required_char_field = {
        'type': "string",
        'maxLength': 250,
    }

    class Meta:
        required = ['required_char_field']


class CharFieldModel(models.Model):
    _schema = Schema()
    data = JSONField(default={})


class Test(TestCase):
    def test_crud(self):
        model = CharFieldModel(char_field='test')
        self.assertIsInstance(
            model._meta.get_field('char_field'),
            models.CharField
        )
        self.assertEqual(model.data, {
            'char_field': 'test',
            'required_char_field': '',
        })
        model.save()

        model = CharFieldModel.objects.get()
        self.assertEqual(model.data, {
            'char_field': 'test',
            'required_char_field': '',
        })
        self.assertEqual(model.char_field, 'test')

    def test_null_value(self):
        model = CharFieldModel()
        self.assertEqual(model.char_field, None)
        self.assertEqual(model.data, {})
