from django.db import models
from django.test import TestCase
import jsonstore


class CharFieldModel(models.Model):
    data = models.JSONField(default=dict)
    char_field = jsonstore.CharField(max_length=250, blank=True)
    required_char_field = jsonstore.CharField(max_length=250)


class Test(TestCase):
    def test_crud(self):
        model = CharFieldModel(char_field='test')
        self.assertIsInstance(
            model._meta.get_field('char_field'),
            models.CharField
        )
        self.assertEqual(model.data, {
            'char_field': 'test',
            # 'required_char_field': '',
        })
        # TODO: Add validation for required fields. Should raise an error on save
        model.save()

        model = CharFieldModel.objects.get()
        self.assertEqual(model.data, {
            'char_field': 'test',
            # 'required_char_field': '',
        })
        self.assertEqual(model.char_field, 'test')

    def test_null_value(self):
        model = CharFieldModel()
        self.assertEqual(model.char_field, None)
        self.assertEqual(model.data, {})

    def test_non_string_assignment_is_coerced_to_string(self):
        model = CharFieldModel.objects.create(char_field=123)

        self.assertEqual(model.data["char_field"], "123")
        fresh = CharFieldModel.objects.get(pk=model.pk)
        self.assertEqual(fresh.char_field, "123")
        self.assertIsInstance(fresh.char_field, str)
