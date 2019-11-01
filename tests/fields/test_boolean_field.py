from django.db import models
from django.test import TestCase
from jsonfield_schema import JSONField, JSONSchema


class Schema(JSONSchema):
    boolean_field = {
        'type': 'boolean'
    }

    class Meta:
        required = ['boolean_field']


class BooleanFieldModel(models.Model):
    _schema = Schema()
    data = JSONField()


class Test(TestCase):
    def test_crud(self):
        model = BooleanFieldModel(boolean_field=False)
        self.assertIsInstance(
            model._meta.get_field('boolean_field'),
            models.BooleanField
        )
        self.assertEqual(model.data, {
            'boolean_field': False
        })
        model.save()

        model = BooleanFieldModel.objects.get()
        self.assertEqual(model.data, {
            'boolean_field': False
        })
        self.assertEqual(model.boolean_field, False)
