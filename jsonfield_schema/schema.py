from functools import partialmethod
from django.db.models import fields
# from django.db.models.query_utils import DeferredAttribute


class JSONSchema(object):
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

    def contribute_to_class(self, cls, name, **kwargs):
        for base_cls in cls.mro():
            if hasattr(base_cls, '_meta'):
                for field in base_cls._meta.fields:
                    if 'name' == field.name:
                        return

        field = self.construct_field({})
        field.contribute_to_class(cls, 'name')

    def construct_field(self, field_def):
        # todo
        return CharField(max_length=250)


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


class NullBooleanField(JSONFieldMixin, fields.NullBooleanField):
    pass


class TextField(JSONFieldMixin, fields.TextField):
    pass


class URLField(JSONFieldMixin, fields.URLField):
    pass
