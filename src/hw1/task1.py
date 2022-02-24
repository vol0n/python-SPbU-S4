from math import sqrt
from copy import deepcopy
from typing import Union, List, Tuple

Num = Union[float, int]
Vector = List[Num]
Matrix = List[List[Num]]


def check_vectors_compatible(vec1: Vector, vec2: Vector):
    if len(vec1) != len(vec2):
        raise ValueError("Vectors should have the same size!")


def calc_product(vec1: Vector, vec2: Vector) -> Num:
    check_vectors_compatible(vec1, vec2)
    return sum(map(lambda x, y: x * y, vec1, vec2))


def calc_len(vec: Vector) -> Num:
    if not vec:
        raise ValueError("Vector should not be empty to calc his len!")
    return sqrt(sum(map(lambda x: x ** 2, vec)))


# actually it return the cos of the angle
def calc_angle(vec1: Vector, vec2: Vector) -> Num:
    check_vectors_compatible(vec1, vec2)
    len1, len2 = calc_len(vec1), calc_len(vec2)
    # if one of the vectors is null, then angle is zero
    if not len1 * len2:
        return 1
    return calc_product(vec1, vec2) / (len1 * len2)


def check_is_matrix(mat: Matrix):
    if len(mat) and not mat:
        return
    assert len(mat), "Minimal matrix is [[]], not []"
    if not all(map(lambda row: len(row) == len(mat[0]), mat)):
        raise ValueError("All rows of a matrix must have the same size.")


def check_matrices_equal_size(mat1: Matrix, mat2: Matrix):
    for mat in (mat1, mat2):
        check_is_matrix(mat)
    if len(mat1) != len(mat2) or len(mat1[0]) != len(mat2[0]):
        raise ValueError("Matrices must have the same size.")


def two_add(mat1: Matrix, mat2: Matrix):
    check_matrices_equal_size(mat1, mat2)
    for i in range(len(mat1)):
        for j in range(len(mat1[0])):
            mat1[i][j] += mat2[i][j]


def add(mat1: Matrix, *args: Matrix) -> Matrix:
    res = deepcopy(mat1)
    for arg in args:
        two_add(res, arg)
    return res


def transpose(mat: Matrix) -> Matrix:
    return [[mat[i][j] for i in range(len(mat))] for j in range(len(mat[0]))]


def mul(mat1: Matrix, mat2: Matrix) -> Matrix:
    for mat in (mat1, mat2):
        check_is_matrix(mat)
    assert mat1 and mat2, "Can't multiply empty matrices!"
    if len(mat1[0]) != len(mat2):
        raise ValueError(f"Wrong sizes for multiplication: {(len(mat1), len(mat1[0]))}, {(len(mat2), len(mat2[0]))}")
    result: List[List[float]] = [
        # could use simply zip(*mat2) to get cols, but then mypy complains that zip returns Iterable[Tuple[Any, ...]]
        [calc_product(row, col) for col in ([row[i] for row in mat2] for i in range(len(mat2[0])))]
        for row in mat1
    ]
    return result
