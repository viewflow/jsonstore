from django.contrib.auth.models import AbstractUser
from polymodels.models import PolymorphicModel
from jsonfield_schema import JSONField
from . import schemas


from polymodels.managers import PolymorphicManager
from django.contrib.auth.models import UserManager


class UserManager(PolymorphicManager, UserManager):
    pass


class User(PolymorphicModel, AbstractUser):
    _schema = schemas.User()
    data = JSONField(null=True)
    objects = UserManager()


class Employee(User):
    _schema = schemas.Employee()

    class Meta:
        proxy = True


class Client(User):
    _schema = schemas.Client()

    class Meta:
        proxy = True
