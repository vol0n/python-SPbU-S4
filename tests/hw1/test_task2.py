import pytest
import src.hw1.task2 as t2


def path_to_str(path) -> str:
    return str(path.absolute())


@pytest.fixture
def empty_file(tmp_path_factory):
    fn = tmp_path_factory.mktemp("data") / "emptyfile.txt"
    with fn.open("w") as f:
        f.write("")
        return path_to_str(fn)


@pytest.fixture
def filewithcontent(tmp_path_factory):
    lines = ["123\n", "45 78\n", "9 11\n"]  # content of a file
    fn = tmp_path_factory.mktemp("data") / "filewithcontent.txt"
    with fn.open("w") as f:
        f.write("".join(lines))
        return path_to_str(fn)


def test_wc_empty(empty_file):
    assert t2.wc(empty_file) == f"0 0 0 {empty_file}"


def test_wc_with_content(filewithcontent):
    assert t2.wc(filewithcontent) == f"3 5 15 {filewithcontent}"


def test_nl_empty(empty_file):
    assert t2.nl(empty_file) == f""


def test_nl_with_content(filewithcontent):
    assert t2.nl(filewithcontent) == "1 123\n2 45 78\n3 9 11\n"


@pytest.mark.parametrize("n, expected", [(0, ""), (1, ""), (100, "")])
def test_head_empty(empty_file, n, expected):
    assert t2.head(empty_file, n) == expected


@pytest.mark.parametrize(
    "n, expected", [(0, ""), (1, "123\n"), (2, "123\n45 78\n"), (3, "123\n45 78\n9 11\n"), (4, "123\n45 78\n9 11\n")]
)
def test_head_with_content(filewithcontent, n, expected):
    assert t2.head(filewithcontent, n) == expected


@pytest.mark.parametrize("n, expected", [(0, ""), (1, ""), (100, "")])
def test_tail_empty(empty_file, n, expected):
    assert t2.tail(empty_file, n) == expected


@pytest.mark.parametrize(
    "n, expected", [(0, ""), (1, "9 11\n"), (2, "45 78\n9 11\n"), (3, "123\n45 78\n9 11\n"), (4, "123\n45 78\n9 11\n")]
)
def test_tail_with_content(filewithcontent, n, expected):
    assert t2.tail(filewithcontent, n) == expected
