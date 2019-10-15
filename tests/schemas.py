from jsonfield_schema import JSONSchema


class Person(JSONSchema):
    name = {
        "type": "string",
        "minLength": 3,
        "maxLength": 250,
    }
    address = {
        "type": "string",
        "maxLength": 250,
    }

    class Meta:
        populate = ['name']
        required = ['name', 'address']


class Client(Person):
    business_phone = {
        "type": "string"
    }

    class Meta(Person.Meta):
        populate = [
            'business_phone'
        ]


class VIPClient(Client):
    approved = {
        "type": "boolean"
    }
    personal_phone = {
        "type": "string"
    }

    class Meta(Person.Meta):
        populate = [
            'approved', 'personal_phone'
        ]
        required = ['approved']
