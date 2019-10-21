from jsonfield_schema import JSONSchema


class User(JSONSchema):
    user_type = {
        "type": "string",
        "enum": ["Employee", "Manager", "Client"],
        "maxLength": 250,
    }

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
    }

    city = {
        "type": "string",
    }

    class Meta:
        populate = ['address', 'zip_code', 'city']
