=======================
Django JSONStore
=======================

IN ORDER TO REDUCE MAINTENANCE COST, THE PACKAGE FUNCTIONALITY WAS MOVED INTO THE
`django-viewflow <https://github.com/viewflow/viewflow>`_

PLEASE, CONSIDE TO UPGRADE AND UPDATE IMPORTS:


.. code:: bash

    $ pip install django-viewflow>=2.0.0b1


.. code:: python

    from viewflow import jsonstore


Description
===========

Expose Django JSONField data as virtual model fields

Use ModelForm and ModelAdmin as usual. Perform simple queries. Migrate to real
table columns when needed without code change.

Suitable to store dumb business data, quick prototypes without DB migrations,
and replace multi-table inheritance joins.

.. image:: https://img.shields.io/pypi/v/django-jsonstore.svg
    :target: https://pypi.python.org/pypi/django-jsonstore

.. image:: https://img.shields.io/pypi/pyversions/django-jsonstore.svg
    :target: https://pypi.python.org/pypi/django-jsonstore

.. image:: https://img.shields.io/pypi/djversions/django-jsonstore.svg
    :target: https://pypi.python.org/pypi/django-jsonstore

*Use with caution! Replacing relational structures with JSON data should be
mindfull architecture decision.*

Works with any JSONField `django.contrib.postgres <https://docs.djangoproject.com/en/2.2/ref/contrib/postgres/fields/#jsonfield>`_,
`django-annoying <https://github.com/skorokithakis/django-annoying#jsonfield>`_,
`django-mysql <https://django-mysql.readthedocs.io/en/latest/model_fields/json_field.html>`_,
upcoming django `Cross-db JSONField <https://github.com/django/django/pull/11452>`_

*Work in progress* part of https://json-schema.org definitions are only supported.

Quick start
===========

.. code:: python

    import jsonstore
    from django import forms
    from django.contrib import admin
    from django.db import models
    from .??. import JSONField

    class Employee(models.Model):
        data = JSONField(default={})
        full_name = jsonstore.CharField(max_length=250)
        hire_date = jsonstore.DateField()
        salary = jsonstore.DecimalField(max_digits=10, decimal_places=2)

    class EmployeeForm(forms.ModelForm):
        class Meta:
            model = Employee
            fields = ['full_name', 'hire_date', 'salary']

    @admin.register(Employee)
    class EmployeeAdmin(admin.ModelAdmin):
        list_display = ['full_name', 'hire_date']
        fields = ['full_name', ('hire_date', 'salary')]


Demo
====

The demo shows how to handle multiple User types within single table with
JSONField and `Django-Polymodels <https://github.com/charettes/django-polymodels/>`_ proxies.

.. code:: bash

   $ export DATABASE_URL=postgresql://viewflow:viewflow@localhost/viewflow
   $ export DJANGO_SETTINGS_MODULE=demo.settings
   $ tox python manage.py migrate
   $ tox python manage.py runserver


License
=======

Django JSONStore is an Open Source project licensed under the terms of
the AGPL license - `The GNU Affero General Public License v3.0
<http://www.gnu.org/licenses/agpl-3.0.html>`_ with the Additional Permissions
described in `LICENSE_EXCEPTION <./LICENSE_EXCEPTION>`_

You can more read about AGPL at `AGPL FAQ <http://www.affero.org/oagf.html>`_
This package license scheme follows to GCC Runtime library licensing. If you use
Linux already, probably this package license, should not bring anything new to
your stack.

Latest changelog
================

0.5.1 2023-01-16
----------------

Package deprication on favor of django-viewflow
