import os.path


def check_exists(file_path: str):
    if not os.path.exists(file_path):
        raise ValueError(f"path to non-existing file: {file_path}")


def wc(file_path: str) -> str:
    check_exists(file_path)
    line_count = word_count = byte_count = 0
    with open(file_path) as f:
        for line in f:
            line_count += 1
            word_count += len(line.split(" "))
            byte_count += len(line)

    return f"{line_count} {word_count} {byte_count} {file_path}"


def nl(file_path: str) -> str:
    check_exists(file_path)
    newlines = []
    line_number = 1
    with open(file_path) as f:
        for line in f:
            newlines.append(f"{line_number} {line}")
            line_number += 1
    return "".join(newlines)


def head(file_path: str, n: int) -> str:
    check_exists(file_path)
    lines = []
    with open(file_path) as f:
        for idx, line in enumerate(f):
            if n < idx + 1:
                break
            lines.append(line)
    return "".join(lines)


def tail(file_path: str, n: int) -> str:
    check_exists(file_path)
    with open(file_path) as f:
        lines = f.readlines()
        if len(lines) < n:
            n = len(lines)
        return "".join(lines[len(lines) - n :] if n else "")
