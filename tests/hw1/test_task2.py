from pathlib import Path
import pytest
import src.hw1.task2 as t2


def path_to_str(path: Path) -> str:
    return str(path.absolute())


def create_file(path: Path, content="", name="file.txt") -> str:
    fn = path / name
    with fn.open("w") as f:
        f.write(content)
    return path_to_str(fn)


@pytest.fixture
def tmp_dir(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("data")


@pytest.fixture
def empty_file(tmp_dir: Path) -> str:
    return create_file(tmp_dir, "", "empty_file.txt")


@pytest.fixture
def filewithcontent(tmp_dir: Path) -> str:
    lines = ["123\n", "45 78\n", "9 11\n"]  # content of a file
    return create_file(tmp_dir, "".join(lines), "filewithcontent.txt")


def test_wc_empty(empty_file):
    assert t2.wc(empty_file) == f"0 0 0 {empty_file}"


def test_wc_with_content(filewithcontent):
    assert t2.wc(filewithcontent) == f"3 5 15 {filewithcontent}"


def test_nl_empty(empty_file):
    assert t2.nl(empty_file) == f""


def test_nl_with_content(filewithcontent):
    assert t2.nl(filewithcontent) == "1 123\n2 45 78\n3 9 11\n"


def test_nl_dont_count_empty_lines(tmp_dir: Path):
    content = """
line 1

line 2
    """.strip(
        "\n"
    )
    temp_file_path: str = create_file(tmp_dir, content, "fileWithEmptyLines.txt")
    assert (
        t2.nl(temp_file_path)
        == """
1 line 1

2 line 2
    """.strip(
            "\n"
        )
    )


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
