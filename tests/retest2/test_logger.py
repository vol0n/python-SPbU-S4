from pathlib import Path
from src.retest2.logcall import logger


def test_format(tmp_path: Path):
    log_file = tmp_path / "foo.txt"

    @logger(log_file)
    def foo(*args, **kwargs):
        pass

    foo(1, 2, a=1)

    assert log_file.read_text().endswith("foo (1, 2) (a=1) None\n")


def test_multiple_calls(tmp_path: Path):
    log_file = tmp_path / "foo1.txt"

    @logger(log_file)
    def foo(n, **kwargs):
        if n != 0:
            foo(n - 1, **kwargs)

    foo(2, uu="g")

    lines = log_file.read_text().splitlines()
    print(lines)
    assert len(lines) == 3
    assert lines[0].endswith("foo (0,) (uu=g) None")
    assert lines[1].endswith("foo (1,) (uu=g) None")
    assert lines[2].endswith("foo (2,) (uu=g) None")
