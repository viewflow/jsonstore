from jsonfield_schema import JSONSchema


class User(JSONSchema):
    class Meta:
        populate = []


class Employee(User):
    hire_date = {
        "type": "string",
        "format": "date"
    }

    salary = {
        "type": "number",
        "multiplyOf": 0.01,
    }

    department = {
        "type": "string",
        "enum": ["Marketing", "Development", "Sales"],
        "maxLength": 250,
    }

    class Meta:
        populate = ['hire_date', 'salary', 'department']


class Client(User):
    address = {
        "type": "string",
    }

    zip_code = {
        "type": "string",
        "maxLength": 250,
    }

    city = {
        "type": "string",
        "maxLength": 250,
    }

    vip = {
        "type": "boolean",
    }

    class Meta:
        populate = ['address', 'zip_code', 'city', 'vip']
