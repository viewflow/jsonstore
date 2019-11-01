from django.db import models
from django.test import TestCase
from jsonfield_schema import JSONField, JSONSchema


class Schema(JSONSchema):
    nullboolean_field = {
        'type': 'boolean'
    }


class NullBooleanFieldModel(models.Model):
    _schema = Schema()
    data = JSONField()


class Test(TestCase):
    def test_crud(self):
        model = NullBooleanFieldModel(nullboolean_field=False)
        self.assertIsInstance(
            model._meta.get_field('nullboolean_field'),
            models.NullBooleanField
        )
        self.assertEqual(model.data, {
            'nullboolean_field': False
        })
        model.save()

        model = NullBooleanFieldModel.objects.get()
        self.assertEqual(model.data, {
            'nullboolean_field': False
        })
        self.assertEqual(model.nullboolean_field, False)

    def test_null_value(self):
        model = NullBooleanFieldModel(nullboolean_field=None)
        self.assertEqual(model.nullboolean_field, None)
        self.assertEqual(model.data, {
            'nullboolean_field': None
        })
