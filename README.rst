=======================
Django JSONField-Schema
=======================

Expose JSONField data as a virtual django model fields.

Use ModelForm and ModelAdmin as usual. Perform simple queries. Migrate to real
table columns when needed without code change.


*Work in progress* part of https://json-schema.org definitions are only supported.

Quick start
===========

.. code:: python

    from django import forms
    from django.contrib import admin
    from django.db import models
    from jsonfield_schema import JSONSchema

    class EmployeeSchema(JSONSchema):
        full_name = {
            "type": "string"
        }

        hire_date = {
            "type": "string",
            "format": "date"
        }

        salary = {
            "type": "number",
            "multiplyOf": 0.01,
        }

    class Employee(models.Model):
        _schema = EmployeeSchema()
        data = JSONField()

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

.. code:: bash

   $ export DATABASE_URL=postgresql://viewflow:viewflow@localhost/viewflow
   $ export DJANGO_SETTINGS_MODULE=demo.settings
   $ tox python manage.py migrate
   $ tox python manage.py runserver
