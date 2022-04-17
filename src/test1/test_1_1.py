from typing import Callable
from datetime import datetime
from functools import wraps
from inspect import signature


def spy(func: Callable) -> Callable:
    func.__dict__["_is_spy"] = True
    func.__dict__["_statistics"] = []

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(args)
        print(kwargs)
        params = {}
        for i, p in enumerate(signature(func).parameters):
            if i >= len(args):
                break
            params[p] = args[i]
        for k, v in kwargs.items():
            params[k] = v
        func.__dict__["_statistics"].append((datetime.now().time(), params))
        func(*args, **kwargs)

    return wrapper


def print_usage_statistics(func: Callable):
    if "_is_spy" not in func.__dict__:
        raise ValueError("Expected a decorated @spy function!")
    generator = (tupl for tupl in func.__dict__["_statistics"])
    return generator
