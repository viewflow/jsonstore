from .fields import (
    JSONField,
    BooleanField, CharField, DateField, DateTimeField,
    DecimalField, EmailField, FloatField,
    IntegerField, IPAddressField, GenericIPAddressField,
    NullBooleanField, TextField, TimeField, URLField
)


__all__ = (
    'JSONField',
    'BooleanField', 'CharField', 'DateField', 'DateTimeField',
    'DecimalField', 'EmailField', 'FloatField',
    'IntegerField', 'IPAddressField', 'GenericIPAddressField',
    'NullBooleanField', 'TextField', 'TimeField', 'URLField'
)


import warnings

warnings.warn("The package was merged into django-viewflow. Please consider to switch to django-viewflow>=2.0.0b1")