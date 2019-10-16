from django.contrib.auth.models import AbstractUser
from jsonfield_schema import JSONField
from . import managers, schemas


class User(AbstractUser):
    _schema = schemas.User()
    data = JSONField()

    objects = managers.UserManager()


class Employee(User):
    _schema = schemas.Employee()

    class Meta:
        proxy = True


class Manager(Employee):
    _schema = schemas.Manager()

    class Meta:
        proxy = True


class Client(User):
    _schema = schemas.Client()

    class Meta:
        proxy = True
