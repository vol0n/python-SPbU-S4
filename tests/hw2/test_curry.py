import pytest
import src.hw2.task as t
from typing import Callable


def apply_curried_func(curried_func: Callable, count: int, args: list):
    f = curried_func
    for i in range(count):
        f = f(args[i])
    return f if args else f()


@pytest.mark.parametrize(
    "func, arity, args, expected",
    [
        (lambda x, y, z: f"<{x},{y},{z}>", 3, [123, 456, 562], "<123,456,562>"),
        (min, 2, [2, 3], 2),
        (len, 1, [[]], 0),
        (lambda: "u", 0, [], "u"),
    ],
)
def test_curry_result(func: Callable, arity: int, args: list, expected):
    f = t.curry_explicit(func, arity)
    assert apply_curried_func(f, arity, args) == expected


def test_curry_freezes_vaarg_func():
    curried_print: Callable = t.curry_explicit(print, 3)
    assert curried_print(1)(2)(3) is None


def test_curry_wrong_number_of_agrs():
    with pytest.raises(TypeError):
        curried_func: Callable = t.curry_explicit(min, 2)
        curried_func(1)(2, 3)


def test_curry_negative_arity():
    with pytest.raises(TypeError):
        t.curry_explicit(min, -1)


@pytest.mark.parametrize(
    "func, arity, args, expected",
    [
        (lambda x, y, z: f"<{x},{y},{z}>", 3, [123, 456, 562], "<123,456,562>"),
        (min, 2, [2, 3], 2),
        (len, 1, [[]], 0),
        (lambda: "u", 0, [], "u"),
    ],
)
def test_uncurry_result(func, arity, args, expected):
    curried_f: Callable = t.curry_explicit(func, arity)
    uncurried_f: Callable = t.uncurry_explicit(curried_f, arity)
    assert uncurried_f(*args) == expected


def test_uncurry_raises_with_wrong_number_of_args():
    curried_f: Callable = t.curry_explicit(min, 3)
    uncurried_f: Callable = t.uncurry_explicit(curried_f, 3)
    with pytest.raises(TypeError):
        uncurried_f(1, 2)
