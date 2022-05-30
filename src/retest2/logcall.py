from typing import Callable
from datetime import datetime


def logger(filename: str) -> Callable:
    def decorator(f: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            with open(filename, "a") as fp:
                datetime_string = datetime.now().strftime("%H:%M:%S|%d/%m/%Y")
                kwargs_repr = " ".join(f"{k}={v}" for k, v in kwargs.items())
                fp.write(f"{datetime_string} {f.__name__} {args} ({kwargs_repr}) {result}\n")
            return result

        return wrapper

    return decorator
