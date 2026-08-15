from datetime import date
from django.db import models
from django.test import TestCase
import jsonstore


class DateFieldModel(models.Model):
    data = models.JSONField()
    date_field = jsonstore.DateField(blank=True, null=False)


class Test(TestCase):
    def test_crud(self):
        model = DateFieldModel(date_field=date(2020, 1, 31))
        self.assertIsInstance(
            model._meta.get_field('date_field'),
            models.DateField
        )
        self.assertEqual(model.data, {
            'date_field': '2020-01-31'
        })
        model.save()

        model = DateFieldModel.objects.get()
        self.assertEqual(model.data, {
            'date_field': '2020-01-31'
        })
        self.assertEqual(model.date_field, date(2020, 1, 31))

    def test_null_value(self):
        model = DateFieldModel(date_field=None)
        self.assertEqual(model.date_field, None)
        self.assertEqual(model.data, {})

    def test_string_assignment_is_coerced_to_date(self):
        model = DateFieldModel.objects.create(date_field="2020-01-31")

        self.assertEqual(model.data, {"date_field": "2020-01-31"})
        self.assertEqual(
            DateFieldModel.objects.get(pk=model.pk).date_field, date(2020, 1, 31)
        )

    def test_values_list_returns_date(self):
        DateFieldModel.objects.create(date_field=date(2020, 1, 31))

        value = DateFieldModel.objects.values_list("date_field", flat=True).get()

        self.assertEqual(value, date(2020, 1, 31))
        self.assertIsInstance(value, date)
