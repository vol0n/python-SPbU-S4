import pytest
from src.hw4.Treap import TreapNode


def treap_node_from_list(nodes: list[tuple]):
    """
    construct TreapNode from a list of tuples, list dictates the structure of the tree:
    left[i] = 2*i + 1, right[i] = 2*i + 2

    This is used for creating test TreapNodes
    """

    def add(i):
        if i < len(nodes):
            if not nodes[i]:
                return None
            return TreapNode(*nodes[i], add(2 * i + 1), add(2 * i + 2))
        return None

    return add(0)


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
    assert treap_node_from_list(nodes) == expected


@pytest.mark.parametrize("node, expected", [(TreapNode.NIL_VERTEX, False), (TreapNode(1, 1), True)])
def test_bool_conversion(node, expected):
    assert expected == bool(node)


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
        (TreapNode.NIL_VERTEX, TreapNode(1, 1), TreapNode(1, 1)),
        (TreapNode(1, 1), TreapNode(1, 1), TreapNode(1, 1)),
        (TreapNode(1, 1), TreapNode(2, 2), treap_node_from_list([(2, 2), (1, 1), None])),
        (TreapNode(1, 1), TreapNode(0, 0), treap_node_from_list([(1, 1), (0, 0), None])),
        (TreapNode(1, 1), TreapNode(2, 0), treap_node_from_list([(1, 1), None, (2, 0)])),
        (
            treap_node_from_list([(5, 7), (4, 6), (7, 6)]),
            TreapNode(1, 8),
            treap_node_from_list([(1, 8), None, (5, 7), None, None, (4, 6), (7, 6)]),
        ),
    ],
)
def test_insert(treap, node, expected):
    assert treap.insert(node) == expected


@pytest.mark.parametrize(
    "node, other, expected",
    [
        (TreapNode.NIL_VERTEX, TreapNode.NIL_VERTEX, TreapNode.NIL_VERTEX),
        (TreapNode.NIL_VERTEX, TreapNode(1, 1), TreapNode(1, 1)),
        (TreapNode(0, 0), TreapNode.NIL_VERTEX, TreapNode(0, 0)),
        (
            treap_node_from_list([(3, 10)]),
            treap_node_from_list([(5, 1)]),
            treap_node_from_list([(3, 10), None, (5, 1)]),
        ),
    ],
)
def test_merge(node, other, expected):
    assert expected == node.merge(other)


@pytest.mark.parametrize(
    "treap, key, expected",
    [
        (TreapNode(0, 0), 0, TreapNode.NIL_VERTEX),
        (treap_node_from_list([(5, 5), (3, 3), (6, 6)]), 5, treap_node_from_list([(6, 6), (3, 3), None])),
        (treap_node_from_list([(5, 5), (3, 3), (6, 6)]), 3, treap_node_from_list([(5, 5), None, (6, 6)])),
        (treap_node_from_list([(5, 5), (3, 3), (6, 6)]), 6, treap_node_from_list([(5, 5), (3, 3), None])),
    ],
)
def test_delete(treap, key, expected):
    assert expected == treap.delete(key)


@pytest.mark.parametrize(
    "treap, key", [(TreapNode.NIL_VERTEX, 1), (treap_node_from_list([(3, 3), (2, 2), (4, 4), (1, 1)]), 5)]
)
def test_delete_raises(treap, key):
    with pytest.raises(KeyError):
        treap.delete(key)


@pytest.mark.parametrize(
    "root, key, expected",
    [
        (TreapNode.NIL_VERTEX, 1, (TreapNode.NIL_VERTEX, TreapNode.NIL_VERTEX)),
        (TreapNode(10, 1), 1, (TreapNode.NIL_VERTEX, TreapNode(10, 1))),
        (TreapNode(1, 1), 10, (TreapNode(1, 1), TreapNode.NIL_VERTEX)),
        (TreapNode(10, 12, TreapNode(5, 5)), 7, (TreapNode(5, 5), TreapNode(10, 12))),
        (
            treap_node_from_list([(5, 7), (4, 6), (7, 6)]),
            1,
            (TreapNode.NIL_VERTEX, treap_node_from_list([(5, 7), (4, 6), (7, 6)])),
        ),
    ],
)
def test_split(root, key, expected):
    assert expected == root.split(key)


@pytest.mark.parametrize(
    "treap, expected",
    [
        (None, []),
        (TreapNode(1, 1), [TreapNode(1, 1)]),
        (
            treap_node_from_list([(3, 3), (2, 2), (1, 1)]),
            [treap_node_from_list([(3, 3), (2, 2), (1, 1)]), TreapNode(2, 2), TreapNode(1, 1)],
        ),
    ],
)
def test_walk_direct(treap, expected):
    assert expected == list(TreapNode.walk_direct(treap))
