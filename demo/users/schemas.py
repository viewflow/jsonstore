from jsonfield_schema import JSONSchema


class User(JSONSchema):
    user_type = {
        "type": "string"
        # choices
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


class Manager(Employee):
    department = {
        "type": "string",
        # choices
    }


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
