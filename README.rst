================
Django JSONStore
================

Expose Django ``JSONField`` data as virtual model fields.

Declare typed fields on a model as usual. Their values live inside one JSON
column instead of getting a column each. Forms, admin, querying and ordering
work like they do for concrete fields, and no migration is generated -- so you
can add, rename or drop a field without touching the database schema.

.. image:: https://img.shields.io/pypi/v/django-jsonstore.svg
    :target: https://pypi.python.org/pypi/django-jsonstore

.. image:: https://img.shields.io/pypi/pyversions/django-jsonstore.svg
    :target: https://pypi.python.org/pypi/django-jsonstore

.. image:: https://img.shields.io/pypi/djversions/django-jsonstore.svg
    :target: https://pypi.python.org/pypi/django-jsonstore

Good for business data with a shifting shape, quick prototypes that shouldn't
generate a migration per idea, and models that would otherwise need multi-table
inheritance. When a field settles down, rename it to a real column and drop the
``jsonstore.`` prefix -- the rest of your code keeps working.

**Documentation:** https://docs.viewflow.io/orm/json_storage.html

The full reference lives on the Viewflow documentation site. `django-viewflow
<https://github.com/viewflow/viewflow>`_ depends on this package and re-exports
it as ``viewflow.jsonstore``, so ``from viewflow import jsonstore`` and
``import jsonstore`` give you the same classes. What follows is a tour.

*Replacing relational structures with JSON documents is an architecture
decision. Foreign keys stored in a document have no database constraint, and
neither do unique or many-to-many relations. Read the Limitations section
before you reach for the relation fields.*


Installation
============

.. code:: bash

    $ pip install django-jsonstore

There is no app to add to ``INSTALLED_APPS``. Requires Python 3.10+ and a
Django version still under upstream support -- 5.2 LTS, 6.0 or 6.1.


Quick start
===========

.. code:: python

    import jsonstore
    from decimal import Decimal
    from django import forms
    from django.contrib import admin
    from django.db import models

    class Employee(models.Model):
        data = models.JSONField(default=dict)

        full_name = jsonstore.CharField(max_length=250)
        hire_date = jsonstore.DateField()
        salary = jsonstore.DecimalField(max_digits=10, decimal_places=2)

    employee = Employee(full_name="Ann Lee", salary=Decimal("100.00"))
    employee.data
    # {"full_name": "Ann Lee", "salary": "100.00"}

The model behaves like any other. The virtual fields are available to
ModelForms, the admin, ``values()``/``values_list()``, ``filter()`` and
``order_by()``:

.. code:: python

    class EmployeeForm(forms.ModelForm):
        class Meta:
            model = Employee
            fields = ["full_name", "hire_date", "salary"]

    @admin.register(Employee)
    class EmployeeAdmin(admin.ModelAdmin):
        list_display = ["full_name", "hire_date"]
        fields = ["full_name", ("hire_date", "salary")]

    Employee.objects.filter(full_name="Ann Lee").order_by("hire_date")
    Employee.objects.values_list("full_name", flat=True)


Field types
===========

Every field takes the same arguments as its ``django.db.models`` counterpart --
``max_length``, ``default``, ``null``, ``blank``, ``choices``, ``verbose_name``,
``help_text`` and so on.

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
``DecimalField``               string, exact -- no float rounding
``DateField``                  ``YYYY-MM-DD``
``DateTimeField``              ISO 8601, made timezone-aware
``TimeField``                  ISO 8601
``DurationField``              ISO 8601 duration
``UUIDField``                  string
``BinaryField``                base64 string
``JSONField``                  any JSON value, nested freely
============================== ============================================

Values that aren't JSON-native round-trip through the field's own
serialization, so a ``DecimalField`` gives back a ``Decimal`` and a
``DateField`` a ``date`` -- not the string sitting in the column.


Custom keys and nesting
=======================

By default a field is stored under its own name inside a JSON column named
``data``. Both are configurable.

``json_field_name`` selects which JSON column holds the value, so one model can
spread its virtual fields across several columns:

.. code:: python

    class Employee(models.Model):
        public = models.JSONField(default=dict)
        private = models.JSONField(default=dict)

        full_name = jsonstore.CharField(max_length=250, json_field_name="public")
        ssn = jsonstore.CharField(max_length=20, json_field_name="private")

``json_key`` overrides the key used inside that column. Pass a string for a
custom key, or a list/tuple for a nested path -- intermediate dicts are created
as needed, and several fields can share a parent:

.. code:: python

    class Person(models.Model):
        data = models.JSONField(default=dict)

        full_name = jsonstore.CharField(max_length=250, json_key="name")
        city = jsonstore.CharField(max_length=100, json_key=("address", "city"))
        zip_code = jsonstore.CharField(max_length=10, json_key=("address", "zip"))

    Person(full_name="Ann", city="Paris", zip_code="75001").data
    # {"name": "Ann", "address": {"city": "Paris", "zip": "75001"}}

The custom key is used everywhere -- reading, writing, filtering
(``Person.objects.filter(city="Paris")``, ``filter(city__isnull=True)``) and
ordering (``order_by("city")``). It works with every field type, relations
included.


Foreign keys
============

``jsonstore.ForeignKey`` stores the related object's primary key in the JSON
column under ``<name>_id``. ``instance.<name>`` returns the related object,
loaded lazily and cached; ``instance.<name>_id`` gives the raw pk.

.. code:: python

    class Book(models.Model):
        data = models.JSONField(default=dict)
        title = jsonstore.CharField(max_length=250)
        author = jsonstore.ForeignKey(Author, null=True, blank=True)

    book = Book(title="Pale Fire", author=nabokov)
    book.data        # {"title": "Pale Fire", "author_id": 1}
    book.author      # <Author: Nabokov>
    book.author_id   # 1

Lazy ``"app.Model"`` references work, and so does any primary key type -- an
integer or a ``UUIDField`` pk is stored in its JSON-native form and coerced
back on read. ``formfield()`` is a ``ModelChoiceField``, so the field drops
into ModelForms and the admin unchanged.

``jsonstore.OneToOneField`` behaves the same on the forward side.

Because the value lives in a document there is no database-level foreign key
constraint: ``on_delete`` has no effect, no reverse accessor is added to the
target model, and there are no joins. Query through the JSON key instead:

.. code:: python

    Book.objects.filter(data__author_id=nabokov.pk)

``filter(author__name=...)`` and ``select_related`` are not available.


Many-to-many
============

``jsonstore.ManyToManyField`` keeps the relation as a list of primary keys
inside the JSON column -- no join table. ``instance.<name>`` returns a manager
with the familiar related-manager API:

.. code:: python

    class Post(models.Model):
        data = models.JSONField(default=dict)
        tags = jsonstore.ManyToManyField(Tag)

    post.tags.set([python, django])   # data == {"tags": [1, 2]}
    post.tags.add(json)
    post.tags.remove(python)
    post.tags.count()                 # 2
    list(post.tags.all())             # [<Tag: django>, <Tag: json>]
    post.save()                       # the manager only edits the document

``formfield()`` yields a ``ModelMultipleChoiceField``; a selection made through
a form is persisted for you. ``all()`` is a ``filter(pk__in=[...])`` queryset,
so it comes back in database order rather than insertion order. Membership
queries go through the JSON key and depend on the backend, e.g. on PostgreSQL:

.. code:: python

    Post.objects.filter(data__tags__contains=[django.pk])


Embedded documents
==================

For structured sub-data, declare a schema-only ``jsonstore.EmbeddedModel`` --
typed fields, no table of its own -- and embed an instance with
``jsonstore.EmbeddedField``:

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

Reading ``product.price`` returns an instance bound to the stored
sub-document, so ``product.price.amount = 120`` is persisted by the next
``product.save()``. An ``EmbeddedModel`` accepts every typed field above, honors
``json_key`` inside its document, and can hold another ``EmbeddedField`` for
deeper nesting.

For a list of documents use ``jsonstore.EmbeddedListField``:

.. code:: python

    class Order(models.Model):
        data = models.JSONField(default=dict)
        lines = jsonstore.EmbeddedListField(LineItem)

    order.lines = [LineItem(sku="a", qty=1), LineItem(sku="b", qty=2)]
    order.lines.append(LineItem(sku="c", qty=3))
    order.lines[0].qty = 5          # in-place edit, persisted on save()
    len(order.lines)                # 3

``instance.<name>`` is a mutable, list-like accessor -- indexing, slicing,
iteration, ``len``, ``append``, ``insert``, ``del``. Query the nested values
through the raw JSON key:

.. code:: python

    Product.objects.filter(data__price__amount=100)

django-viewflow builds on these two fields to edit an embedded document as a
nested form and a list of them as inlines, through ``EmbeddedModelForm`` /
``EmbeddedFormField`` / ``EmbeddedFormSetField``. See
`Editing embedded documents as forms
<https://docs.viewflow.io/orm/json_storage.html>`_.


Polymorphic models
==================

Virtual fields combine well with `proxy models
<https://docs.djangoproject.com/en/stable/topics/db/models/#proxy-models>`_:
different real-life object types over one table, without multi-table
inheritance.

.. code:: python

    class User(PolymorphicModel, AbstractUser):
        data = models.JSONField(default=dict)

    class Client(User):
        address = jsonstore.CharField(max_length=250)
        city = jsonstore.CharField(max_length=250)
        vip = jsonstore.BooleanField()

        class Meta:
            proxy = True


Migrating to a real column
==========================

When a field earns its own column, drop the ``jsonstore.`` prefix and run
``makemigrations``. Add a data migration to copy the values out of the JSON
document; nothing else in your code has to change.


Supported databases
===================

PostgreSQL 12+, MySQL 8+, MariaDB 10.5+, Oracle 21c+ and SQLite 3.38+.

Django's own ``JSONField`` does the storage, so the requirements match
`Django's <https://docs.djangoproject.com/en/stable/ref/models/fields/#jsonfield>`_.
Querying a virtual field compiles to a key transform on the JSON column, so the
database has to be able to index into the document.


Limitations
===========

* No database constraints. A ``jsonstore.ForeignKey`` will happily point at a
  deleted row; ``on_delete`` does nothing, and ``OneToOneField`` has no
  ``UNIQUE`` index.
* No reverse accessors, no joins, no ``select_related`` /
  ``prefetch_related``.
* Relation managers and embedded accessors mutate the in-memory document only.
  Call ``instance.save()`` afterwards.
* No indexes on virtual fields unless you add a functional index on the JSON
  column yourself. Filtering scans the document.
* ``EmbeddedListField`` has no ``through`` model and no ordering guarantee
  beyond list order.


Contributing
============

``make test`` runs the suite; ``make help`` lists the rest of the targets,
including running it against each supported database and across the Django
version matrix.


License
=======

Django JSONStore is an Open Source project licensed under the terms of
the AGPL license - `The GNU Affero General Public License v3.0
<http://www.gnu.org/licenses/agpl-3.0.html>`_ with the Additional Permissions
described in `LICENSE_EXCEPTION <./LICENSE_EXCEPTION>`_

You can read more about AGPL at `AGPL FAQ <http://www.affero.org/oagf.html>`_.
This package's license scheme follows GCC Runtime Library licensing. If you use
Linux already, this license should not bring anything new to your stack.


Changelog
=========

See `CHANGELOG.rst <./CHANGELOG.rst>`_. Full documentation:
https://docs.viewflow.io/orm/json_storage.html
