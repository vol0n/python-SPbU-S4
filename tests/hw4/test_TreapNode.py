from __future__ import annotations

import pytest
from src.hw4.Treap import TreapNode, K, split, merge
from typing import Any, Union, Optional


def is_treap(node: Optional[TreapNode]) -> bool:
    if not node:
        return True
    res = True
    if node.left:
        res = res and node.left.key < node.key and node.left.y <= node.y and is_treap(node.left)
    if node.right:
        res = res and node.key < node.right.key and node.right.y <= node.y and is_treap(node.right)
    return res


TupleNode = Union[tuple[K, Any, float], tuple[K, Any]]


def from_tuples(node: TupleNode, *nodes: TupleNode) -> TreapNode[K]:
    res = TreapNode(*node)
    for node in nodes:
        res = res.insert(TreapNode(*node))
    return res


@pytest.mark.parametrize(
    "node, expected",
    [
        (TreapNode(1, 1), "(1, 1)"),
        (
            from_tuples((7, None, 8), (5, None, 4), (10, None, 5)),
            """
     ____(7, None)_____     
     |                |     
(5, None)         (10, None)""".strip(
                "\n"
            ),
        ),
    ],
)
def test_repr(node, expected):
    assert expected == node.__repr__()


@pytest.mark.parametrize(
    "treap, node, expected",
    [
        (TreapNode(1, 1), TreapNode(1, 1), TreapNode(1, 1)),
        (TreapNode(1, "1"), TreapNode(2, 2), from_tuples((1, "1"), (2, 2))),
        (TreapNode(1, 1), TreapNode(0, 1), from_tuples((1, 1), (0, 1))),
        (TreapNode(1, 1), TreapNode(2, 0), from_tuples((1, 1), (2, 0))),
        (from_tuples((4, 6), (7, 6), (5, 7)), TreapNode(1, 8), from_tuples((4, 6), (7, 6), (5, 7), (1, 8))),
    ],
)
def test_insert(treap, node, expected):
    assert is_treap(treap) and is_treap(node)

    new_treap = treap.insert(node)
    assert is_treap(new_treap) and new_treap == expected


@pytest.mark.parametrize(
    "node, other, expected",
    [
        (None, None, None),
        (None, TreapNode(1, 1), TreapNode(1, 1)),
        (TreapNode(0, 0), None, TreapNode(0, 0)),
        (TreapNode(3, 10), TreapNode(5, 1), from_tuples((3, 10), (5, 1))),
    ],
)
def test_merge(node, other, expected):
    assert is_treap(node) and is_treap(other) and is_treap(expected)
    assert expected == merge(node, other)


@pytest.mark.parametrize(
    "treap, key, expected",
    [
        (TreapNode(0, 0), 0, None),
        (from_tuples((5, 5), (3, 3), (6, 6)), 5, from_tuples((6, 6), (3, 3))),
        (from_tuples((5, 5), (3, 3), (6, 6)), 3, from_tuples((5, 5), (6, 6))),
        (from_tuples((5, 5), (3, 3), (6, 6)), 6, from_tuples((5, 5), (3, 3))),
    ],
)
def test_delete(treap, key, expected):
    assert is_treap(treap) and is_treap(expected)
    new_treap_node = treap.delete(key)
    assert is_treap(new_treap_node)
    assert expected == new_treap_node


@pytest.mark.parametrize("treap, key", [(from_tuples((3, 3), (2, 2), (4, 4), (1, 1)), 5)])
def test_delete_raises(treap, key):
    with pytest.raises(KeyError):
        treap.delete(key)


@pytest.mark.parametrize(
    "root, key, expected",
    [
        (None, 1, (None, None)),
        (TreapNode(10, 1), 1, (None, TreapNode(10, 1))),
        (TreapNode(1, 1), 10, (TreapNode(1, 1), None)),
        (from_tuples((10, 12), (5, 5)), 7, (TreapNode(5, 5), TreapNode(10, 12))),
        (
            from_tuples((5, 7), (4, 6), (7, 6)),
            1,
            (None, from_tuples((5, 7), (4, 6), (7, 6))),
        ),
    ],
)
def test_split(root, key, expected):
    def check_split(treap1: Optional[TreapNode[K]], treap2: Optional[TreapNode[K]], k):
        assert is_treap(treap1) and is_treap(treap2)
        if treap1:
            for node in treap1.walk_direct():
                assert node.key <= k
        if treap2:
            for node in treap2.walk_direct():
                assert k <= node.key

    tr1, tr2 = split(root, key)
    check_split(tr1, tr2, key)
    assert expected == (tr1, tr2)


@pytest.mark.parametrize(
    "treap, expected",
    [
        (TreapNode(1, 1), [TreapNode(1, 1)]),
        (
            from_tuples((3, 3, 3), (2, 2, 2), (1, 1, 1)),
            [from_tuples((3, 3, 3), (2, 2, 2), (1, 1, 1)), from_tuples((2, 2, 2), (1, 1, 1)), TreapNode(1, 1)],
        ),
    ],
)
def test_walk_direct(treap, expected):
    assert expected == list(TreapNode.walk_direct(treap))
