import pytest
from src.test1.test_1_1 import *


def test_args():
    @spy
    def foo1(x):
        print(f"f1 was called with {x}")

    foo1(10)
    foo1(20)

    stats = list(print_usage_statistics(foo1))
    assert len(stats) == 2
    assert stats[0][1]["x"] == 10
    assert stats[1][1]["x"] == 20


def test_def_args():
    @spy
    def foo(x=1):
        pass

    foo(2)
    foo("a")
    foo(x=10)
    stats = list(print_usage_statistics(foo))
    assert len(stats) == 3
    assert stats[0][1]["x"] == 2
    assert stats[1][1]["x"] == "a"
    assert stats[2][1]["x"] == 10
