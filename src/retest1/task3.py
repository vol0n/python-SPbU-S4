from inspect import signature
from datetime import datetime
from typing import Callable
import os


def create_log_message(func: Callable, excepton: Exception, *args, **kwargs) -> str:
    params = {}
    for i, p in enumerate(signature(func).parameters):
        if i >= len(args):
            break
        params[p] = args[i]

    for k, v in kwargs.items():
        params[k] = v
    params_repr = " ".join(f"{k}={v}" for k, v in params.items())

    return (
        f"{datetime.now().time()} function {getattr(callable, '__name__', repr(func))} failed with exception: \n"
        + f"{excepton}. \nArguments: {params_repr}"
    )


def write_log_message(message: str, file_path: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "a") as f:
        f.write(message)


def safe_call(path: str):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                write_log_message(create_log_message(func, e, *args, **kwargs), path)
                return None

        return wrapper

    return decorator
