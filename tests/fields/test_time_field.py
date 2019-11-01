from datetime import time
from django.db import models
from django.test import TestCase
from jsonfield_schema import JSONField, JSONSchema


class Schema(JSONSchema):
    time_field = {
        'type': 'string',
        'format': 'time',
    }


class TimeFieldModel(models.Model):
    _schema = Schema()
    data = JSONField()


class Test(TestCase):
    def test_crud(self):
        model = TimeFieldModel(time_field=time(12, 59))
        self.assertIsInstance(
            model._meta.get_field('time_field'),
            models.TimeField
        )
        self.assertEqual(model.data, {
            'time_field': '12:59:00+00:00'
        })
        model.save()

        model = TimeFieldModel.objects.get()
        self.assertEqual(model.data, {
            'time_field': '12:59:00+00:00'
        })
        self.assertEqual(model.time_field, time(12, 59))

    def test_null_value(self):
        model = TimeFieldModel(time_field=None)
        self.assertEqual(model.time_field, None)
        self.assertEqual(model.data, {})
