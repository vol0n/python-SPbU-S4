import pytest
import src.test2.task2 as t2


def check_sorted(array):
    is_ok = True
    for i in range(1, len(array)):
        is_ok = (array[i] >= array[i-1])
        if not is_ok:
            break
    return is_ok


@pytest.mark.parametrize("array, numproc, expected", [
    ([], (1, 2, 3), []),
    ([1], (1, 2), [1]),
    ([8, 0, 1, 45, 1], (1, 2), [0, 1, 1, 8, 45])
])
def test_sort(array, numproc, expected):
    for n in numproc:
        data = list(array)
        print(f"testing on {data} with {n} processes")
        t2.quicksort(data, 0, len(array)-1, n)
        assert data == expected