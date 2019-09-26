from django.db import models
from json_store.fields import JSONField


class Order(models.Model):
    data = JSONField()


class Person(models.Model):
    class Schema:
        name = {
            "type": "string",
        }
        address = {
            "type": "string"
        }


class Client(models.Model):
    class Schema(Person.Schema):
        business_phone = {
            "type": "string"
        }
