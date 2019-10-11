from django.db import models
from jsonfield_schema import JSONField
from . import schemas


class Order(models.Model):
    data = JSONField()


class Person(models.Model):
    _schema = schemas.Person()
    data = JSONField()


class Client(Person):
    _schema = schemas.Client()


class VIPClient(Client):
    _schema = schemas.VIPClient()

    class Meta:
        proxy = True
