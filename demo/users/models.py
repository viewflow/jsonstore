from django.contrib.auth.models import AbstractUser
from django.urls import reverse
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

    def get_absolute_url(self):
        return reverse('employee_edit', args=[self.pk])

    class Meta:
        proxy = True


class Client(User):
    _schema = schemas.Client()

    def get_absolute_url(self):
        return reverse('client_edit', args=[self.pk])

    class Meta:
        proxy = True
