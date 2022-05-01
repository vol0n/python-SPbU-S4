import pytest
from src.test1.test_1_task2 import *


def test_simple_fun():
    @takes(int)
    def foo(x):
        pass

    with pytest.raises(TypeError):
        foo("1")

    foo(1)


def test_keyword_args():
    @takes(int)
    def foo(x):
        pass

    with pytest.raises(TypeError):
        foo(x="1")

    foo(1)


def test_both():
    @takes(int, str)
    def bar(a, b):
        pass

    with pytest.raises(TypeError):
        bar(1, b=1)


def test_raises_when_too_many_types():
    with pytest.raises(ValueError):

        @takes(int, int)
        def foo():
            pass
