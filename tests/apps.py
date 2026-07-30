import os

from django.apps import AppConfig


class TestsConfig(AppConfig):
    name = "tests"
    path = os.path.dirname(os.path.abspath(__file__))
    default_auto_field = "django.db.models.AutoField"
