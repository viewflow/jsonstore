import jsonstore
from django.db import models


class Order(models.Model):
    data = jsonstore.JSONField()


class Person(models.Model):
    data = jsonstore.JSONField()
    name = jsonstore.CharField(max_length=250)
    address = jsonstore.CharField(max_length=250, blank=True)


class Client(Person):
    birthdate = jsonstore.DateField()
    business_phone = jsonstore.CharField(max_length=250)


class VIPClient(Client):
    approved = jsonstore.BooleanField()
    personal_phone = jsonstore.CharField(max_length=250)

    class Meta:
        proxy = True
