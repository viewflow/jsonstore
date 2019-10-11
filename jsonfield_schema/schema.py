from functools import partialmethod
from django.db.models import fields
# from django.db.models.query_utils import DeferredAttribute


class CharField(fields.CharField):
    concrete = False

    def contribute_to_class(self, cls, name, private_only=False):
        self.set_attributes_from_name(name)
        self.model = cls
        self.concrete = False
        self.column = None
        cls._meta.add_field(self, private=True)

        # TODO descriptior!!
        # if self.column:
        #     if not getattr(cls, self.attname, None):
        #         setattr(cls, self.attname, DeferredAttribute(self.attname))

        if self.choices is not None:
            setattr(cls, 'get_%s_display' % self.name,
                    partialmethod(cls._get_FIELD_display, field=self))


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

        field = CharField(max_length=250)
        field.contribute_to_class(cls, 'name')
        # cls._meta.add_field(field, private=True)
