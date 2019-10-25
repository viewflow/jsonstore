from importlib import import_module

import django
from django.conf import settings


def JSONField(*args, **kwargs):
    """
    Returns json field implementation depends on the
    default db connection type or `db_vendor` keyword argument
    """
    db_vendor = kwargs.pop('db_vendor', None)
    if db_vendor is None:
        backend = import_module('{}.base'.format(settings.DATABASES['default']['ENGINE']).replace('_psycopg2', ''))
        db_vendor = backend.DatabaseWrapper.vendor

    if db_vendor == 'postgresql':
        from django.contrib.postgres.fields import JSONField as PG_JSONField
        return PG_JSONField(*args, **kwargs)
    elif db_vendor == 'mysql':
        try:
            from django_mysql.models import JSONField as MY_JSONField
        except ImportError:
            raise ImportError("django-mysql isn't installed")
        else:
            return MY_JSONField(*args, **kwargs)
    elif db_vendor == 'oracle':
        try:
            from oracle_json_field.fields import JSONField as OR_JSONField
        except ImportError:
            raise ImportError("oracle-json-field isn't installed")
        else:
            return OR_JSONField(*args, **kwargs)
    else:
        if django.VERSION >= (3, 0):
            # Quick six for django-annoying
            import six
            from django import utils
            utils.six = six

        try:
            from annoying.fields import JSONField as DEFAULT_JSONField
        except ImportError:
            raise ImportError("django-annoying isn't installed")
        else:
            return DEFAULT_JSONField(*args, **kwargs)
