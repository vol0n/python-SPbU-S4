import pytest
from src.hw4.Treap import TreapNode


@pytest.mark.parametrize(
    "nodes, expected",
    [
        ([], None),
        ([(1, 1)], TreapNode(1, 1)),
        ([(7, 8), (5, 4), (10, 5)], TreapNode(7, 8, TreapNode(5, 4), TreapNode(10, 5))),
        ([(3, 10), None, (5, 1)], TreapNode(3, 10, None, TreapNode(5, 1))),
    ],
)
def test_from_list(nodes, expected):
    assert TreapNode.from_list(nodes) == expected


@pytest.mark.parametrize(
    "node, expected",
    [
        (TreapNode(1, 1), "(1, 1)"),
        (
            TreapNode(7, 8, TreapNode(5, 4), TreapNode(10, 5)),
            """
   ___(7, 8)___    
   |          |    
(5, 4)      (10, 5)
""".strip(
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
        (None, TreapNode(1, 1), TreapNode(1, 1)),
        (TreapNode(1, 1), TreapNode(1, 1), TreapNode(1, 1)),
        (TreapNode(1, 1), TreapNode(2, 2), TreapNode.from_list([(2, 2), (1, 1), None])),
        (TreapNode(1, 1), TreapNode(0, 0), TreapNode.from_list([(1, 1), (0, 0), None])),
        (TreapNode(1, 1), TreapNode(2, 0), TreapNode.from_list([(1, 1), None, (2, 0)])),
        (
            TreapNode.from_list([(5, 7), (4, 6), (7, 6)]),
            TreapNode(1, 8),
            TreapNode.from_list([(1, 8), None, (5, 7), None, None, (4, 6), (7, 6)]),
        ),
    ],
)
def test_insert(treap, node, expected):
    assert TreapNode.insert(treap, node) == expected


@pytest.mark.parametrize(
    "fst, snd, expected",
    [
        (None, None, None),
        (None, TreapNode(1, 1), TreapNode(1, 1)),
        (TreapNode(0, 0), None, TreapNode(0, 0)),
        (TreapNode.from_list([(3, 10)]), TreapNode.from_list([(5, 1)]), TreapNode.from_list([(3, 10), None, (5, 1)])),
    ],
)
def test_merge(fst, snd, expected):
    assert TreapNode.merge(fst, snd) == expected


@pytest.mark.parametrize(
    "treap, key, expected",
    [
        (TreapNode(0, 0), 0, None),
        (TreapNode.from_list([(5, 5), (3, 3), (6, 6)]), 5, TreapNode.from_list([(6, 6), (3, 3), None])),
        (TreapNode.from_list([(5, 5), (3, 3), (6, 6)]), 3, TreapNode.from_list([(5, 5), None, (6, 6)])),
        (TreapNode.from_list([(5, 5), (3, 3), (6, 6)]), 6, TreapNode.from_list([(5, 5), (3, 3), None])),
    ],
)
def test_delete(treap, key, expected):
    assert expected == TreapNode.delete(treap, key)


@pytest.mark.parametrize("treap, key", [(None, 1), (TreapNode.from_list([(3, 3), (2, 2), (4, 4), (1, 1)]), 5)])
def test_delete_raises(treap, key):
    with pytest.raises(KeyError):
        TreapNode.delete(treap, key)


@pytest.mark.parametrize(
    "root, key, expected",
    [
        (None, 1, (None, None)),
        (TreapNode(10, 1), 1, (None, TreapNode(10, 1))),
        (TreapNode(1, 1), 10, (TreapNode(1, 1), None)),
        (TreapNode(10, 12, TreapNode(5, 5)), 7, (TreapNode(5, 5), TreapNode(10, 12))),
        (TreapNode.from_list([(5, 7), (4, 6), (7, 6)]), 1, (None, TreapNode.from_list([(5, 7), (4, 6), (7, 6)]))),
    ],
)
def test_split(root, key, expected):
    assert expected == TreapNode.split(root, key)


@pytest.mark.parametrize(
    "treap, expected",
    [
        (None, []),
        (TreapNode(1, 1), [TreapNode(1, 1)]),
        (
            TreapNode.from_list([(3, 3), (2, 2), (1, 1)]),
            [TreapNode.from_list([(3, 3), (2, 2), (1, 1)]), TreapNode(2, 2), TreapNode(1, 1)],
        ),
    ],
)
def test_walk_direct(treap, expected):
    assert expected == list(TreapNode.walk_direct(treap))
