=========
Changelog
=========

26.8.0
------

- Coerce virtual field values through Django's ``to_python()`` conversion on
  reads and writes, including values already present in JSON documents.
- Return the declared Python types from ``values()`` and ``values_list()`` for
  typed fields such as dates, durations and UUIDs.
- Evaluate callable defaults once and materialize them on first access for
  model and embedded fields.
- Reject ``ForeignKey`` assignments whose value is not an instance of the
  related model.


26.7.0
------

The package is maintained again, and versioning switches to CalVer
(``YY.MM.MICRO``). Everything that grew inside ``django-viewflow`` while
``django-jsonstore`` was deprecated has moved back here, and
``django-viewflow`` now depends on this package -- ``from viewflow import
jsonstore`` keeps working and resolves to the same classes.

New since 0.5.1:

- Relations stored in the document: ``ForeignKey``, ``OneToOneField`` and
  ``ManyToManyField``. Related objects load lazily and are cached, any primary
  key type works (integer or ``UUIDField``), lazy ``"app.Model"`` targets
  resolve, and ``formfield()`` gives a ``ModelChoiceField`` /
  ``ModelMultipleChoiceField`` so they work in ModelForms and the admin.
  ``ManyToManyField`` exposes ``all``/``add``/``remove``/``set``/``clear``/
  ``count`` and persists a form selection.
- Embedded documents: ``EmbeddedModel`` declares a schema-only virtual model,
  ``EmbeddedField`` stores one as a nested document and ``EmbeddedListField``
  stores a list of them. Both bind to the stored sub-document, so in-place
  edits persist on ``save()``.
- ``json_key`` places a field under a custom key or a nested path
  (``json_key=("address", "city")``), used consistently for reads, writes,
  filtering and ordering. ``json_field_name`` spreads a model's virtual fields
  across several JSON columns.
- ``order_by()`` on a virtual field now sorts by the extracted value instead of
  the JSON blob's text representation.
- New field types: ``BigIntegerField``, ``SmallIntegerField``,
  ``PositiveIntegerField``, ``PositiveSmallIntegerField``,
  ``PositiveBigIntegerField``, ``SlugField``, ``FilePathField``,
  ``BinaryField`` (base64), ``DurationField``, ``UUIDField`` and ``JSONField``.
- Django's built-in ``models.JSONField`` is the only storage backend. The
  third-party JSONField shims and the ``queryset`` module are gone.

Supports only Django versions still under upstream support -- 5.2 LTS, 6.0 and
6.1 -- on Python 3.10+. The suite passes on SQLite, PostgreSQL 17, MySQL 8.4,
MariaDB 11 and Oracle 23ai. On MariaDB and Oracle, ``order_by()`` on a numeric
virtual field sorts the extracted value as text; those two assertions are
skipped there.


0.5.1 2023-01-16
----------------

Package deprication on favor of django-viewflow


0.5.0 2020-12-31
----------------

Support for Django 3.1 JSONField

0.4.1 2019-11-07
----------------

* Fix boolean field


0.4.0 2019-11-07
----------------

* Whole idea simplified. The library renamed to 'jsonstore'


0.3.0 2019-11-01
----------------

* Support for date/time/datetime values
* Support for help_text (description) and verbose_name (verboseName) field specs


0.2.0 2019-10-25
----------------

* Support for Python 2.7 and django 1.11/3.0


0.1.0 2019-10-21
----------------

* Initial Release
