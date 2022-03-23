from src.hw4.Treap import Treap, TreapNode
import pytest


@pytest.mark.parametrize(
    "treap, expected", [(Treap(), {}), (Treap({1: 1}), {1: 1}), (Treap({1: 2, 3: 1}), {3: 1, 1: 2})]
)
def test_to_dict(treap, expected):
    assert treap.to_dict() == expected


@pytest.mark.parametrize(
    "init_dict, expected",
    [
        ({}, Treap()),
        ({1: 2}, Treap.from_list([(1, 2)])),
        ({3: 3, 4: 3}, Treap.from_list([(3, 3), None, (4, 3)])),
        ({3: 3, 2: 2, 1: 1}, Treap.from_list([(3, 3), (2, 2), None, (1, 1), None])),
    ],
)
def test_constructor(init_dict, expected):
    assert Treap(init_dict) == expected


@pytest.mark.parametrize(
    "treap, expected_walk",
    [
        (Treap(), []),
        (Treap({1: 2}), [TreapNode(1, 2)]),
        (Treap({3: 3, 4: 3}), [TreapNode.from_list([(3, 3), None, (4, 3)]), TreapNode(4, 3)]),
    ],
)
def test_iter(treap, expected_walk):
    assert list(iter(treap)) == expected_walk


@pytest.mark.parametrize("treap, key, expected", [(Treap({1: 1}), 1, 1), (Treap({1: 2, 3: 4, 5: 5, 6: 6}), 6, 6)])
def test_get_item(treap, key, expected):
    assert treap[key] == expected


@pytest.mark.parametrize("treap, key", [(Treap(), 1), (Treap({1: 1, 2: 3}), 3)])
def test_get_item_raises(treap, key):
    with pytest.raises(KeyError):
        treap[key]


@pytest.mark.parametrize(
    "treap, key, item, expected",
    [(Treap(), 1, 1, Treap({1: 1})), (Treap({1: 1}), 1, 1, Treap({1: 1})), (Treap({1: 1}), 1, 3, Treap({1: 3}))],
)
def test_set_item(treap, key, item, expected):
    treap[key] = item
    assert treap == expected


@pytest.mark.parametrize(
    "treap, key,expected",
    [
        (Treap(), 1, False),
        (Treap({1: 2}), 1, True),
        (Treap({1: 1, 2: 4, 5: 6, 7: 10}), 7, True),
        (Treap({1: 1, 2: 4, 5: 6, 7: 10}), 10, False),
    ],
)
def test_in_operator(treap, key, expected):
    assert (key in treap) == expected


@pytest.mark.parametrize(
    "treap, key, expected",
    [(Treap({1: 1}), 1, Treap()), (Treap({1: 1, 2: 4, 5: 6, 7: 10}), 7, Treap({1: 1, 2: 4, 5: 6}))],
)
def test_del_operator(treap, key, expected):
    del treap[key]
    assert treap == expected


@pytest.mark.parametrize("treap, key", [(Treap({1: 1}), 2), (Treap({1: 1, 2: 4, 5: 6, 7: 10}), 11)])
def test_del_operator_raises(treap, key):
    with pytest.raises(KeyError):
        del treap[key]
