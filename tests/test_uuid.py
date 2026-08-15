import uuid

from django.db import models
from django.test import TestCase
import jsonstore


class UUIDFieldModel(models.Model):
    data = models.JSONField(default=dict)
    uid = jsonstore.UUIDField(null=True)
    generated_uid = jsonstore.UUIDField(default=uuid.uuid4)


class Test(TestCase):
    def test_roundtrip(self):
        value = uuid.uuid4()
        UUIDFieldModel.objects.create(uid=value)

        obj = UUIDFieldModel.objects.get()
        # stored JSON-native (a string), read back as a UUID
        self.assertEqual(obj.data, {"uid": str(value)})
        self.assertEqual(obj.uid, value)
        self.assertIsInstance(obj.uid, uuid.UUID)

    def test_none(self):
        obj = UUIDFieldModel()

        self.assertIsNone(obj.uid)
        self.assertEqual(obj.data, {})

    def test_assign_string_form(self):
        value = uuid.uuid4()
        obj = UUIDFieldModel(uid=str(value))
        obj.save()

        self.assertEqual(obj.data, {"uid": str(value)})
        self.assertEqual(UUIDFieldModel.objects.get().uid, value)

    def test_callable_default_is_stable_and_materialized_on_access(self):
        obj = UUIDFieldModel()

        first = obj.generated_uid
        second = obj.generated_uid

        self.assertEqual(first, second)
        self.assertEqual(obj.data["generated_uid"], str(first))

    def test_values_list_returns_uuid(self):
        value = uuid.uuid4()
        UUIDFieldModel.objects.create(uid=value)

        projected = UUIDFieldModel.objects.values_list("uid", flat=True).get()

        self.assertEqual(projected, value)
        self.assertIsInstance(projected, uuid.UUID)
