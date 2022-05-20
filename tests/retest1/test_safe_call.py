from src.retest1.task3 import safe_call
from pathlib import Path


def test_file_created_and_not_empty(tmp_path: Path):
    path: Path = tmp_path / "foo_log1.txt"

    @safe_call(str(path))
    def foo(a, b=2):
        if a % 2 == 0:
            return
        raise ValueError("Expected even!")

    foo(1)

    assert path.exists()
    assert len(path.read_text()) > 0


def test_file_not_created_when_no_exception(tmp_path: Path):
    path: Path = tmp_path / "foo_log2.txt"

    @safe_call(str(path))
    def foo(a, b=2):
        if a % 2 == 0:
            return
        raise ValueError("Expected even!")

    foo(2)
    foo(4)

    assert not path.exists()
