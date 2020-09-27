import json
from functools import wraps


def to_json(function):
    "Return a JSON string representation of a function result"
    @wraps(function)
    def wrapper(*args, **kwargs):
        return json.JSONEncoder().encode(function(*args, **kwargs))
    return wrapper
