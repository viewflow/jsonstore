import copy
import math

try:
    from functools import partialmethod
except ImportError:
    # python 2.7
    from functools import partial

    class partialmethod(partial):
        # https://gist.github.com/carymrobbins/8940382
        def __get__(self, instance, owner):
            if instance is None:
                return self
            return partial(self.func, instance,
                           *(self.args or ()), **(self.keywords or {}))


from datetime import date, datetime
from six import with_metaclass

import django
from django.core.exceptions import FieldError
from django.core.validators import (
    MaxValueValidator, MinValueValidator, MinLengthValidator,
    RegexValidator
)
from django.db.models import fields
from django.utils import dateparse, timezone


class JSONSchemaMetaClass(type):
    def __new__(cls, class_name, bases, attrs):
        super_new = super(JSONSchemaMetaClass, cls).__new__

        # Ensure initialization is only performed for subclasses of JSONSchema
        # (excluding JSONSchema class itself).
        parents = [b for b in bases if isinstance(b, JSONSchemaMetaClass)]
        if not parents:
            return super_new(cls, class_name, bases, attrs)

        local_defs = [
            (attr_name, schema_def) for attr_name, schema_def in attrs.items()
            if isinstance(schema_def, dict)
        ]

        attrs['_local_defs'] = local_defs

        return super_new(cls, class_name, bases, attrs)


class JSONSchema(with_metaclass(JSONSchemaMetaClass, object)):  # NOQA
    # Field flags
    auto_created = False
    concrete = False
    editable = False
    hidden = False

    is_relation = False
    many_to_many = False
    many_to_one = False
    one_to_many = False
    one_to_one = False
    related_model = None
    remote_field = None

    attname = None
    column = None

    def __init__(self, json_field_name='data'):
        self.json_field_name = json_field_name

    class Meta:
        pass

    def contribute_to_class(self, cls, name, **kwargs):
        base_fields = [
            field.name for base_cls in cls.mro()
            if hasattr(base_cls, '_meta')
            for field in base_cls._meta.fields
        ]

        populate = getattr(self.Meta, 'populate', None)
        for attr_name, schema_def in self._local_defs:
            if populate is not None and attr_name not in populate:
                continue
            assert attr_name not in base_fields
            field = self.construct_field(attr_name, schema_def)
            if field:
                field.contribute_to_class(cls, attr_name)

    def construct_field(self, field_name, field_def):
        field_kwargs = {
            'json_field_name': self.json_field_name,
            'blank': field_name not in getattr(self.Meta, 'required', []),
        }
        if field_def.get('description'):
            field_kwargs['help_text'] = field_def['description']
        if field_def.get('verboseName'):
            field_kwargs['verbose_name'] = field_def['verboseName']

        field_type = field_def.get('type', None)
        field_format = field_def.get('format', None)
        if field_type == 'string' and field_format is None:
            min_length = field_def.get('minLength', None)
            max_length = field_def.get('maxLength', None)
            pattern = field_def.get('pattern', None)

            validators = []
            if min_length:
                validators.append(MinLengthValidator(min_length))
            if pattern:
                validators.append(RegexValidator(regex=pattern))

            if max_length is None:
                return TextField(
                    validators=validators,
                    **field_kwargs
                )
            else:
                return CharField(
                    max_length=max_length,
                    validators=validators,
                    **field_kwargs
                )
        elif field_type == 'string' and field_format == 'date':
            return DateField(
                **field_kwargs
            )
        elif field_type == 'string' and field_format == 'time':
            return TimeField(
                **field_kwargs
            )
        elif field_type == 'string' and field_format == 'date-time':
            return DateTimeField(
                **field_kwargs
            )
        elif field_type == 'string' and field_format == 'email':
            return EmailField(
                **field_kwargs
            )
        elif field_type == 'string' and field_format == 'ipv4':
            return IPAddressField(
                **field_kwargs
            )
        elif field_type == 'string' and field_format == 'ipv6':
            return GenericIPAddressField(
                **field_kwargs
            )
        elif field_type == 'string' and field_format == 'uri':
            return URLField(
                **field_kwargs
            )
        elif field_type == 'integer':
            return IntegerField(
                **field_kwargs
            )
        elif field_type == 'number':
            maximum = field_def.get('maximum', None)
            minimum = field_def.get('minimum', None)
            multiple_of = field_def.get('multipleOf', None)

            validators = []
            if minimum:
                validators.append(MinValueValidator(maximum))
            if maximum:
                validators.append(MaxValueValidator(maximum))

            if multiple_of:
                decimal_places = -int(math.log10(multiple_of))
                max_digits = math.log10(maximum)+decimal_places if maximum else 42

                return DecimalField(
                    max_digits=max_digits,
                    decimal_places=decimal_places,
                    **field_kwargs
                )
            else:
                return FloatField(
                    **field_kwargs
                )
        elif field_type == 'boolean':
            if field_kwargs['blank']:
                return NullBooleanField(
                    **field_kwargs
                )
            else:
                return BooleanField(
                    **field_kwargs
                )

        return None


class JSONFieldDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        json_value = getattr(instance, self.field.json_field_name)
        if isinstance(json_value, dict):
            value = json_value.get(self.field.attname, None)
            if hasattr(self.field, 'from_json'):
                value = self.field.from_json(value)
            return value
        return None

    def __set__(self, instance, value):
        json_value = getattr(instance, self.field.json_field_name)
        if json_value:
            assert isinstance(json_value, dict)
        else:
            json_value = {}

        if hasattr(self.field, 'to_json'):
            value = self.field.to_json(value)

        if not value and self.field.blank and not self.field.null:
            try:
                del json_value[self.field.attname]
            except KeyError:
                pass
        else:
            json_value[self.field.attname] = value

        setattr(instance, self.field.json_field_name, json_value)


class JSONFieldMixin(object):
    """
    Override django.db.model.fields.Field.contribute_to_class
    to make a field always private, and register custom access descriptor
    """
    def __init__(self, *args, **kwargs):
        self.json_field_name = kwargs.pop('json_field_name', 'data')
        super(JSONFieldMixin, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, private_only=False):
        self.set_attributes_from_name(name)
        self.model = cls
        self.concrete = False
        self.column = self.json_field_name
        cls._meta.add_field(self, private=True)

        if not getattr(cls, self.attname, None):
            descriptor = JSONFieldDescriptor(self)
            setattr(cls, self.attname, descriptor)

        if self.choices is not None:
            setattr(cls, 'get_%s_display' % self.name,
                    partialmethod(cls._get_FIELD_display, field=self))

    def get_lookup(self, lookup_name):
        # Always return None, to make get_transform been called
        return None

    def get_transform(self, name):
        class TransformFactoryWrapper:
            def __init__(self, json_field, transform, original_lookup):
                self.json_field = json_field
                self.transform = transform
                self.original_lookup = original_lookup

            def __call__(self, lhs, **kwargs):
                lhs = copy.copy(lhs)
                lhs.target = self.json_field
                lhs.output_field = self.json_field
                transform = self.transform(lhs, **kwargs)
                transform._original_get_lookup = transform.get_lookup
                transform.get_lookup = lambda name: transform._original_get_lookup(self.original_lookup)
                return transform

        json_field = self.model._meta.get_field(self.json_field_name)
        transform = json_field.get_transform(self.name)
        if transform is None:
            raise FieldError(
                "JSONField '%s' has no support for key '%s' %s lookup" %
                (self.json_field_name, self.name, name)
            )

        return TransformFactoryWrapper(json_field, transform, name)


class BooleanField(JSONFieldMixin, fields.BooleanField):
    def __init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(self, *args, **kwargs)
        if django.VERSION < (2, ):
            self.blank = False


class CharField(JSONFieldMixin, fields.CharField):
    pass


class DateField(JSONFieldMixin, fields.DateField):
    def to_json(self, value):
        if value:
            assert isinstance(value, (datetime, date))
            return value.strftime('%Y-%m-%d')

    def from_json(self, value):
        if value is not None:
            return dateparse.parse_date(value)


class DateTimeField(JSONFieldMixin, fields.DateTimeField):
    def to_json(self, value):
        if value:
            if not timezone.is_aware(value):
                value = timezone.make_aware(value)
            return value.isoformat()

    def from_json(self, value):
        if value:
            return dateparse.parse_datetime(value)


class DecimalField(JSONFieldMixin, fields.DecimalField):
    pass


class EmailField(JSONFieldMixin, fields.EmailField):
    pass


class FloatField(JSONFieldMixin, fields.FloatField):
    pass


class IntegerField(JSONFieldMixin, fields.IntegerField):
    pass


class IPAddressField(JSONFieldMixin, fields.IPAddressField):
    pass


class GenericIPAddressField(JSONFieldMixin, fields.GenericIPAddressField):
    pass


class NullBooleanField(JSONFieldMixin, fields.NullBooleanField):
    pass


class TextField(JSONFieldMixin, fields.TextField):
    pass


class TimeField(JSONFieldMixin, fields.TimeField):
    def to_json(self, value):
        if value:
            if not timezone.is_aware(value):
                value = timezone.make_aware(value)
            return value.isoformat()

    def from_json(self, value):
        if value:
            return dateparse.parse_time(value)


class URLField(JSONFieldMixin, fields.URLField):
    pass
