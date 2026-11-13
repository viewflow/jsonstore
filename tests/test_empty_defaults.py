from django.db import models
from django.test import TestCase

import jsonstore


class EmptyDefaultsModel(models.Model):
    data = models.JSONField(default=dict)
    text = jsonstore.TextField(blank=True, default="")
    optional = jsonstore.CharField(max_length=20, blank=True, default=None)
    generated = jsonstore.CharField(max_length=20, blank=True, default=str)
    nested = jsonstore.CharField(
        max_length=20, blank=True, default="", json_key=("profile", "label")
    )


class EmptyDefaultsEmbedded(jsonstore.EmbeddedModel):
    text = jsonstore.TextField(blank=True, default="")
    optional = jsonstore.CharField(max_length=20, blank=True, default=None)
    generated = jsonstore.CharField(max_length=20, blank=True, default=str)
    nested = jsonstore.CharField(
        max_length=20, blank=True, default="", json_key=("profile", "label")
    )


class EmptyDefaultsTest(TestCase):
    def assert_empty_defaults(self, obj):
        for name, expected in (
            ("text", ""),
            ("optional", None),
            ("generated", ""),
            ("nested", ""),
        ):
            with self.subTest(field=name):
                self.assertEqual(getattr(obj, name), expected)
                self.assertEqual(getattr(obj, name), expected)

    def test_model_defaults_after_reload(self):
        obj = EmptyDefaultsModel.objects.create()
        obj.refresh_from_db()
        self.assert_empty_defaults(obj)
        self.assertEqual(obj.data, {"profile": {}})

    def test_embedded_defaults(self):
        obj = EmptyDefaultsEmbedded()
        self.assert_empty_defaults(obj)
        self.assertEqual(obj._store, {"profile": {}})
