================
Django JSONStore
================

Store flexible model data in JSON without giving up Django fields.

Django JSONStore maps typed model fields to keys inside one
``models.JSONField``. The fields work on model instances, in ModelForms and the
admin. They also support filters, ordering and projections. They do not create
database columns or migrations.

Use it when records need different attributes or those attributes change
often. Your code keeps Django field conversion, validation and form widgets.
You do not have to handle an untyped dictionary.

.. image:: https://img.shields.io/pypi/v/django-jsonstore.svg
    :target: https://pypi.python.org/pypi/django-jsonstore

.. image:: https://img.shields.io/pypi/pyversions/django-jsonstore.svg
    :target: https://pypi.python.org/pypi/django-jsonstore

.. image:: https://img.shields.io/pypi/djversions/django-jsonstore.svg
    :target: https://pypi.python.org/pypi/django-jsonstore

Documentation: https://docs.viewflow.io/orm/json_storage.html


Installation
============

.. code:: bash

    $ pip install django-jsonstore

Do not add an application to ``INSTALLED_APPS``. The package needs Python 3.10
or later, and Django 5.2, 6.0 or 6.1.


Quick start
===========

.. code:: python

    from decimal import Decimal

    from django.db import models
    import jsonstore

    class Employee(models.Model):
        data = models.JSONField(default=dict)

        full_name = jsonstore.CharField(max_length=250)
        hire_date = jsonstore.DateField()
        salary = jsonstore.DecimalField(max_digits=10, decimal_places=2)

    employee = Employee(full_name="Ann Lee", salary=Decimal("100.00"))
    employee.data
    # {"full_name": "Ann Lee", "salary": "100.00"}

The values live in ``data``, but application code uses them as fields.

.. code:: python

    employee.full_name
    # "Ann Lee"

    Employee.objects.filter(full_name="Ann Lee").order_by("hire_date")
    Employee.objects.values_list("full_name", flat=True)


When to use it
==============

JSONStore is a good fit when:

* a model has many optional attributes;
* different records need different sets of attributes;
* attributes change more often than the database schema;
* ModelForms and the admin still need typed Django fields;
* a field may move to a regular database column later.

Use a regular model field if you need a database constraint, index or relation
join. See `Limitations`_ for the trade-offs.


Forms and admin
===============

List virtual fields in ModelForms and ``ModelAdmin`` classes.

.. code:: python

    from django import forms
    from django.contrib import admin

    class EmployeeForm(forms.ModelForm):
        class Meta:
            model = Employee
            fields = ["full_name", "hire_date", "salary"]

    @admin.register(Employee)
    class EmployeeAdmin(admin.ModelAdmin):
        list_display = ["full_name", "hire_date"]
        fields = ["full_name", ("hire_date", "salary")]


Field types
===========

Each field takes the same arguments as the equivalent field in
``django.db.models``. This includes ``max_length``, ``default``, ``null``,
``blank``, ``choices``, ``verbose_name`` and ``help_text``.

============================== ============================================
Field                          Stored as
============================== ============================================
``BooleanField``               JSON boolean
``NullBooleanField``           JSON boolean or null
``CharField``                  string
``TextField``                  string
``EmailField``                 string
``SlugField``                  string
``URLField``                   string
``FilePathField``              string
``IPAddressField``             string
``GenericIPAddressField``      string
``IntegerField``               number
``BigIntegerField``            number
``SmallIntegerField``          number
``PositiveIntegerField``       number
``PositiveBigIntegerField``    number
``PositiveSmallIntegerField``  number
``FloatField``                 number
``DecimalField``               string, with no loss of precision
``DateField``                  ``YYYY-MM-DD``
``DateTimeField``              ISO 8601, with a time zone
``TimeField``                  ISO 8601
``DurationField``              ISO 8601 duration
``UUIDField``                  string
``BinaryField``                base64 string
``JSONField``                  any JSON value
============================== ============================================

A field converts its value when it reads the document. A ``DecimalField``
returns a ``Decimal``, and a ``DateField`` returns a ``date``.


Custom keys and nesting
=======================

A field uses its own name as the key, in a JSON column with the name ``data``.
You can change both.

``json_field_name`` selects the JSON column. One model can keep its virtual
fields in more than one column.

.. code:: python

    class Employee(models.Model):
        public = models.JSONField(default=dict)
        private = models.JSONField(default=dict)

        full_name = jsonstore.CharField(max_length=250, json_field_name="public")
        ssn = jsonstore.CharField(max_length=20, json_field_name="private")

``json_key`` selects the key in that column. Give a string for a different key,
or a list or tuple for a path. The package makes the intermediate dictionaries.
More than one field can use the same parent key.

.. code:: python

    class Person(models.Model):
        data = models.JSONField(default=dict)

        full_name = jsonstore.CharField(max_length=250, json_key="name")
        city = jsonstore.CharField(max_length=100, json_key=("address", "city"))
        zip_code = jsonstore.CharField(max_length=10, json_key=("address", "zip"))

    Person(full_name="Ann", city="Paris", zip_code="75001").data
    # {"name": "Ann", "address": {"city": "Paris", "zip": "75001"}}

The key applies to all operations. This includes reads, writes, filters such as
``Person.objects.filter(city="Paris")`` and ``filter(city__isnull=True)``, and
``order_by("city")``. Every field type accepts ``json_key``, and this includes
the relation fields.


Foreign keys
============

``jsonstore.ForeignKey`` keeps the primary key of the related object in the
JSON column, under the key ``<name>_id``. ``instance.<name>`` returns the
related object. The package reads the object at first access and then keeps it
in a cache. ``instance.<name>_id`` returns the primary key.

.. code:: python

    class Book(models.Model):
        data = models.JSONField(default=dict)
        title = jsonstore.CharField(max_length=250)
        author = jsonstore.ForeignKey(Author, null=True, blank=True)

    book = Book(title="Pale Fire", author=nabokov)
    book.data        # {"title": "Pale Fire", "author_id": 1}
    book.author      # <Author: Nabokov>
    book.author_id   # 1

A lazy ``"app.Model"`` reference is permitted. A primary key of any type is
permitted. The package keeps an integer as a number, and a ``UUIDField``
primary key as a string, then converts it again at read time.
``formfield()`` returns a ``ModelChoiceField`` for use in ModelForms and in the
admin.

``jsonstore.OneToOneField`` operates in the same way in the forward direction.

The value is in a document, and thus the database has no foreign key
constraint. ``on_delete`` has no effect. The target model gets no reverse
accessor. Joins are not available. Use the JSON key to make a query.

.. code:: python

    Book.objects.filter(data__author_id=nabokov.pk)

``filter(author__name=...)`` and ``select_related`` are not available.


Many-to-many
============

``jsonstore.ManyToManyField`` keeps a list of primary keys in the JSON column.
There is no join table. ``instance.<name>`` returns a manager with the usual
related-manager methods.

.. code:: python

    class Post(models.Model):
        data = models.JSONField(default=dict)
        tags = jsonstore.ManyToManyField(Tag)

    post.tags.set([python, django])   # data == {"tags": [1, 2]}
    post.tags.add(json)
    post.tags.remove(python)
    post.tags.count()                 # 2
    list(post.tags.all())             # [<Tag: django>, <Tag: json>]
    post.save()                       # the manager changes only the document

``formfield()`` returns a ``ModelMultipleChoiceField``. The package writes a
selection made in a form. ``all()`` returns a ``filter(pk__in=[...])`` queryset
in database order, not in the order of the list. A query on the members uses
the JSON key, and the syntax is different for each database. On PostgreSQL, use
this query.

.. code:: python

    Post.objects.filter(data__tags__contains=[django.pk])


Embedded documents
==================

An embedded model holds structured data in a sub-document. Declare the schema
with ``jsonstore.EmbeddedModel``. This class has typed fields and no table. Put
an instance in a model with ``jsonstore.EmbeddedField``.

.. code:: python

    class Money(jsonstore.EmbeddedModel):
        amount = jsonstore.IntegerField()
        currency = jsonstore.CharField(max_length=3, default="USD")

    class Product(models.Model):
        data = models.JSONField(default=dict)
        price = jsonstore.EmbeddedField(Money, null=True, blank=True)

    product.price = Money(amount=100, currency="USD")
    product.data          # {"price": {"amount": 100, "currency": "USD"}}
    product.price.amount  # 100

``product.price`` returns an instance that is attached to the stored
sub-document. Thus ``product.price.amount = 120`` becomes permanent at the next
``product.save()``. An ``EmbeddedModel`` accepts each field type in the table
above. It accepts ``json_key``, and it can contain a second ``EmbeddedField``.

``jsonstore.EmbeddedListField`` holds a list of documents.

.. code:: python

    class Order(models.Model):
        data = models.JSONField(default=dict)
        lines = jsonstore.EmbeddedListField(LineItem)

    order.lines = [LineItem(sku="a", qty=1), LineItem(sku="b", qty=2)]
    order.lines.append(LineItem(sku="c", qty=3))
    order.lines[0].qty = 5          # becomes permanent at the next save()
    len(order.lines)                # 3

``instance.<name>`` returns a list-like object. It permits an index, a slice,
iteration, ``len``, ``append``, ``insert`` and ``del``. Use the JSON key to
query a value in the document.

.. code:: python

    Product.objects.filter(data__price__amount=100)


Polymorphic models
==================

Virtual fields operate with `proxy models
<https://docs.djangoproject.com/en/stable/topics/db/models/#proxy-models>`_.
One table can hold more than one type of object, and multi-table inheritance is
not necessary.

.. code:: python

    class User(PolymorphicModel, AbstractUser):
        data = models.JSONField(default=dict)

    class Client(User):
        address = jsonstore.CharField(max_length=250)
        city = jsonstore.CharField(max_length=250)
        vip = jsonstore.BooleanField()

        class Meta:
            proxy = True


Change to a database column
===========================

To give a field its own column, remove the ``jsonstore.`` prefix and run
``makemigrations``. Write a data migration that copies the values out of the
JSON document. No other code changes are necessary.


Supported databases
===================

PostgreSQL 12+, MySQL 8+, MariaDB 10.5+, Oracle 21c+ and SQLite 3.38+.

Django's ``JSONField`` writes the data. Thus the requirements are the same as
the `requirements of Django
<https://docs.djangoproject.com/en/stable/ref/models/fields/#jsonfield>`_. A
query on a virtual field becomes a key transform on the JSON column, and the
database must be able to read a key in the document.


Limitations
===========

* The database has no constraints on these fields. A ``jsonstore.ForeignKey``
  can point to a row that no longer exists. ``on_delete`` has no effect. An
  ``OneToOneField`` has no ``UNIQUE`` index.
* Reverse accessors, joins, ``select_related`` and ``prefetch_related`` are not
  available.
* A relation manager and an embedded accessor change only the document in
  memory. Call ``instance.save()`` after the change.
* A virtual field has no index. To add one, make a functional index on the JSON
  column. A filter reads each document.
* On MariaDB and Oracle, ``order_by()`` on a numeric field sorts the value as
  text. Thus 10 comes before 2. PostgreSQL, MySQL and SQLite sort numerically.
* ``EmbeddedListField`` has no ``through`` model. The order is the order of the
  list.


License
=======

Django JSONStore is an Open Source project. It uses the AGPL license, `The GNU
Affero General Public License v3.0
<http://www.gnu.org/licenses/agpl-3.0.html>`_, with the additional permissions
in `LICENSE_EXCEPTION <./LICENSE_EXCEPTION>`_.

The exception permits you to use this package in a project that has a license
which is not compatible with the AGPL. A proprietary project is included. Your
own code keeps your own license, and you do not release its source. The
condition is that you do not change the source code of this package.

If you do change this package, the AGPL applies to your modified version of it.

The license scheme is the same as the license scheme of the GCC Runtime
Library. The text above is a summary. Read `LICENSE_EXCEPTION
<./LICENSE_EXCEPTION>`_ for the conditions.


Changelog
=========

See `CHANGELOG.rst <./CHANGELOG.rst>`_.
