from functools import wraps
from inspect import signature
from typing import Any


def takes(*types: type):
    def decorator(function):
        params = list(signature(function).parameters.keys())
        print(params)
        if len(types) > len(params):
            raise ValueError(f"Expected at least {len(params)} types, but got {len(types)}")
        allowed_types = {}
        for i, p in enumerate(params):
            if i < len(types):
                allowed_types[p] = types[i]
            else:
                allowed_types[p] = Any

        @wraps(function)
        def wrapper(*args, **kwargs):
            for i, t in enumerate(types):
                if i < len(args) and not isinstance(args[i], t):
                    raise TypeError(f"expected type {t}, but got {args[i].__class__}")

            for param_name, value in kwargs.items():
                if not isinstance(value, allowed_types[param_name]):
                    raise TypeError(f"expected type {allowed_types[param_name]}, but got {value.__class__}")
            function(*args, **kwargs)

        return wrapper

    return decorator
