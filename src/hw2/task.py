from typing import Callable


def curry_explicit(func: Callable, arity: int) -> Callable:
    if arity < 0:
        raise TypeError("Arity can't be negative!")

    if arity in (0, 1):
        return func

    def curried_func(x):
        def helper(*args):
            if len(args) != arity - 1:
                raise TypeError(f"Wrong number of arguments: have {len(args)} but expected {arity-1}")
            return func(x, *args)

        return curry_explicit(helper, arity - 1)

    return curried_func


def uncurry_explicit(curried_func: Callable, arity: int) -> Callable:
    if arity < 0:
        raise TypeError("Arity can't be negative!")

    def helper(*args):
        if len(args) != arity:
            raise TypeError(f"Wrong number of arguments: have {len(args)} but expected {arity}")
        f = curried_func
        for arg in args:
            f = f(arg)
        return f if args else f()

    return helper
