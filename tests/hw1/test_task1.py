import pytest
import src.hw1.task1 as t1
import math

epsilon = 1e-5


def check_real_equal(a, b):
    return abs(b - a) < epsilon


@pytest.mark.parametrize("vec1,vec2", [([], []), ([1], [1]), ([1, 3], [2, 2])])
def test_check_vectors_compatible_result(vec1, vec2):
    t1.check_vectors_compatible(vec1, vec2)


@pytest.mark.parametrize(
    "vec1,vec2,exception", [([], [1], ValueError), ([1], [1, 2], ValueError)]
)
def test_check_vectors_compatible_exception(vec1, vec2, exception):
    with pytest.raises(exception):
        t1.check_vectors_compatible(vec1, vec2)


@pytest.mark.parametrize(
    "vec1,vec2,expected",
    [([1], [1], 1), ([1, 3], [1, 3], 10), ([1j, 1j], [1, -1], 0), ([], [], 0)],
)
def test_calc_product_result(vec1, vec2, expected):
    assert t1.calc_product(vec1, vec2) == expected


@pytest.mark.parametrize("vec1,vec2,exception", [([1, 2], [1], ValueError)])
def test_calc_product_raises(vec1, vec2, exception):
    with pytest.raises(exception):
        t1.calc_product(vec1, vec2)


@pytest.mark.parametrize(
    "vec,expected", [([1], 1), ([4, 3], 5), ([0, 0, 0], 0), ([0], 0)]
)
def test_calc_len(vec, expected):
    assert t1.calc_len(vec) == expected


@pytest.mark.parametrize("vec,exception", [([], ValueError)])
def test_calc_len_raises(vec, exception):
    with pytest.raises(exception):
        t1.calc_len(vec)


@pytest.mark.parametrize(
    "vec1,vec2,expected",
    [([1, 1], [1, 1], 1), ([0, 1], [1, 0], 0), ([1, 0], [1, math.sqrt(3)], 1 / 2)],
)
def test_calc_angle_result(vec1, vec2, expected):
    assert check_real_equal(t1.calc_angle(vec1, vec2), expected)


@pytest.mark.parametrize(
    "vec1,vec2,exception", [([], [1], ValueError), ([], [], ValueError)]
)
def test_calc_angle_raises(vec1, vec2, exception):
    with pytest.raises(exception):
        t1.calc_angle(vec1, vec2)


@pytest.mark.parametrize(
    "mat", [([[1]]), ([[1], [2]]), ([[1, 2, 3], [1j, 1 + 2j, 1]]), ([[]])]
)
def test_check_is_matrix_not_raises(mat):
    t1.check_is_matrix(mat)


@pytest.mark.parametrize(
    "mat,exception",
    [
        ([[1], [2, 3]], ValueError),
        ([[1], []], ValueError),
        ([1], Exception),
        ([], Exception),
    ],
)
def test_check_is_matrix_raises(mat, exception):
    with pytest.raises(exception):
        t1.check_is_matrix(mat)


@pytest.mark.parametrize(
    "mat1,mat2",
    [
        ([[1]], [["x"]]),
        ([[1], [2]], [[3], [4]]),
        ([[1, 1, 1], [0, 0, 0]], [[0, 0, 0], [0, 0, 0]]),
        ([[]], [[]]),
    ],
)
def test_check_matrices_equal_size_not_raises(mat1, mat2):
    t1.check_matrices_equal_size(mat1, mat2)


@pytest.mark.parametrize(
    "mat1,mat2,exception",
    [([[1]], [["x", "s"]], ValueError), ([[], []], [[]], ValueError)],
)
def test_check_matrices_equal_size_not_raises(mat1, mat2, exception):
    with pytest.raises(exception):
        t1.check_matrices_equal_size(mat1, mat2)


@pytest.mark.parametrize(
    "mat1,mat2,expected",
    [
        ([[1, 2], [1, 1]], [[2, 1], [2, 2]], [[3, 3], [3, 3]]),
        ([[1]], [[1j]], [[1 + 1j]]),
        ([[]], [[]], [[]]),
    ],
)
def test_two_add_result(mat1, mat2, expected):
    t1.two_add(mat1, mat2)
    assert mat1 == expected


@pytest.mark.parametrize(
    "mat1,mat2,mat3,expected",
    [
        ([[1, 2], [1, 1]], [[2, 1], [2, 2]], [[3, 3], [3, 3]], [[6, 6], [6, 6]]),
        ([[1]], [[1]], [[1]], [[3]]),
    ],
)
def test_add_result(mat1, mat2, mat3, expected):
    assert t1.add(mat1, mat2, mat3) == expected


@pytest.mark.parametrize(
    "mat,expected",
    [
        ([[1, 2], [1, 1]], [[1, 1], [2, 1]]),
        ([[3, 3, 3], [1, 1, 1]], [[3, 1], [3, 1], [3, 1]]),
    ],
)
def test_transpose_result(mat, expected):
    assert t1.transpose(mat) == expected


@pytest.mark.parametrize(
    "mat1,mat2,expected",
    [
        ([[1, 0], [0, 1]], [[2, 1], [2, 2]], [[2, 1], [2, 2]]),
        ([[1, 0, 1], [0, 1, 0]], [[2, 2], [2, 2], [2, 2]], [[4, 4], [2, 2]]),
    ],
)
def test_mul_result(mat1, mat2, expected):
    assert t1.mul(mat1, mat2) == expected


@pytest.mark.parametrize(
    "mat1,mat2,exception", [([[]], [[]], ValueError), ([[]], [[1, 2]], ValueError)]
)
def test_mul_raises(mat1, mat2, exception):
    with pytest.raises(exception):
        t1.mul(mat1, mat2)
