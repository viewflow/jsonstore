import math

from functools import partialmethod
from six import with_metaclass

from django.core.validators import (
    MaxValueValidator, MinValueValidator, MinLengthValidator,
    RegexValidator
)
from django.db.models import fields


class JSONSchemaMetaClass(type):
    def __new__(cls, class_name, bases, attrs):
        super_new = super().__new__

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
        field_type = field_def.get('type', None)
        field_format = field_def.get('format', None)
        required = field_name in getattr(self.Meta, 'required', [])
        validators = []

        if field_type == 'string' and field_format is None:
            min_length = field_def.get('minLength', None)
            max_length = field_def.get('maxLength', None)
            pattern = field_def.get('pattern', None)

            if min_length:
                validators.append(MinLengthValidator(min_length))
            if pattern:
                validators.append(RegexValidator(regex=pattern))

            if max_length is None:
                return TextField(
                    blank=not required,
                    validators=validators
                )
            else:
                return CharField(
                    max_length=max_length,
                    blank=not required,
                    validators=validators
                )
        elif field_type == 'string' and field_format == 'date':
            return DateField(blank=not required)
        elif field_type == 'string' and field_format == 'time':
            return TimeField(blank=not required)
        elif field_type == 'string' and field_format == 'date-time':
            return DateTimeField(blank=not required)
        elif field_type == 'string' and field_format == 'email':
            return EmailField(blank=not required)
        elif field_type == 'string' and field_format == 'ipv4':
            return IPAddressField(blank=not required)
        elif field_type == 'string' and field_format == 'ipv6':
            return GenericIPAddressField(blank=not required)
        elif field_type == 'string' and field_format == 'uri':
            return URLField(blank=not required)
        elif field_type == 'integer':
            return IntegerField()
        elif field_type == 'number':
            maximum = field_def.get('maximum', None)
            minimum = field_def.get('minimum', None)
            multiple_of = field_def.get('multipleOf', None)

            if minimum:
                validators.append(MaxValueValidator(maximum))
            if maximum:
                validators.append(MaxValueValidator(maximum))

            if multiple_of:
                decimal_places = -int(math.log10(multiple_of))
                max_digits = math.log10(maximum)+decimal_places if maximum else 42

                return DecimalField(
                    max_digits=max_digits,
                    decimal_places=decimal_places
                )
            else:
                return FloatField()
        elif field_type == 'boolean':
            if required:
                return BooleanField()
            else:
                return NullBooleanField()

        return None


class JSONFieldDescriptor(object):
    def __init__(self, field_name, json_field_name='data'):
        self.field_name = field_name
        self.json_field_name = json_field_name

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        json_value = getattr(instance, self.json_field_name)
        if isinstance(json_value, dict):
            return json_value.get(self.field_name, None)
        return None

    def __set__(self, instance, value):
        json_value = getattr(instance, self.json_field_name)
        if json_value:
            assert isinstance(json_value, dict)
            json_value[self.field_name] = value
        else:
            json_value = {self.field_name: value}
        setattr(instance, self.json_field_name, json_value)


class JSONFieldMixin(object):
    """
    Override django.db.model.fields.Field.contribute_to_class
    to make a field always private, and register custom access descriptor
    """

    def contribute_to_class(self, cls, name, private_only=False):
        print(cls, name)
        self.set_attributes_from_name(name)
        self.model = cls
        self.concrete = False
        self.column = None
        cls._meta.add_field(self, private=True)

        if not getattr(cls, self.attname, None):
            setattr(cls, self.attname, JSONFieldDescriptor(self.attname))

        if self.choices is not None:
            setattr(cls, 'get_%s_display' % self.name,
                    partialmethod(cls._get_FIELD_display, field=self))


class BooleanField(JSONFieldMixin, fields.BooleanField):
    pass


class CharField(JSONFieldMixin, fields.CharField):
    pass


class DateField(JSONFieldMixin, fields.DateField):
    pass


class DateTimeField(JSONFieldMixin, fields.DateTimeField):
    pass


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
    pass


class URLField(JSONFieldMixin, fields.URLField):
    pass
