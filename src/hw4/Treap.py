from __future__ import annotations

from typing import Optional, Tuple, TypeVar, Generic, Iterator, Dict, Any, Protocol, Callable
from abc import abstractmethod
import random

K = TypeVar("K", bound="Comparable")


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self, other: K) -> bool:
        pass

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass


class TreapNode(Generic[K]):
    class NilNodeDescriptor:
        def __get__(self, instance, owner) -> TreapNode[K]:
            if '_nil' not in TreapNode.__dict__:
                ins = super().__new__(TreapNode)
                ins.key = ins.value = ins.y = ins.right = ins.left = None
                TreapNode._nil = ins
            return TreapNode._nil

    NIL_VERTEX: TreapNode[K] = NilNodeDescriptor()

    @classmethod
    def from_dict(cls, data: Dict[K, Any]):
        res = TreapNode.NIL_VERTEX
        for k, v in data.items():
            res = res.insert(TreapNode(k, v))
        return res

    def __init__(self, key: K, value: Any, y: float = random.random()):
        self.key: K = key
        self.value: Any = value
        self.y: float = y
        self.right = self.left = TreapNode.NIL_VERTEX

    def __bool__(self) -> bool:
        """
        in expression 'if treap_node:' evaluate to true only if it is not a nil node
        """
        return self is not TreapNode.NIL_VERTEX

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TreapNode):
            return False
        return self.to_dict() == other.to_dict()

    def _print_tree(self) -> list[str]:
        if not self:
            return []

        node_repr = f"({self.key}, {self.value})"
        node_w = len(node_repr)

        left_repr = self.left._print_tree()
        left_w = len(left_repr[0]) if left_repr else 0
        left_h = len(left_repr)

        right_repr = self.right._print_tree()
        right_w = len(right_repr[0]) if right_repr else 0
        right_h = len(right_repr)

        new_repr = [
            " " * (left_w - left_w // 2)
            + "_" * (left_w // 2)
            + node_repr
            + "_" * (right_w // 2)
            + " " * (right_w - right_w // 2)
        ]
        new_w = left_w + node_w + right_w
        if self.left or self.right:
            second_line = [" "] * new_w
            if self.left:
                second_line[left_w - left_w // 2] = "|"
            if self.right:
                second_line[new_w - right_w + right_w // 2 - 1] = "|"
            new_repr.append("".join(second_line))

        i = 0
        while i < left_h and i < right_h:
            new_repr.append(left_repr[i] + " " * node_w + right_repr[i])
            i += 1
        while i < left_h:
            new_repr.append(left_repr[i] + " " * (node_w + right_w))
            i += 1
        while i < right_h:
            new_repr.append(" " * (node_w + left_w) + right_repr[i])
            i += 1
        return new_repr

    def __repr__(self) -> str:
        return "\n".join(TreapNode._print_tree(self))

    def insert(self, node: TreapNode[K]) -> TreapNode[K]:
        if not self or self.key == node.key:
            return node
        if self.y < node.y:
            node.left, node.right = self.split(node.key)
            return node
        if self.key < node.key:
            self.right = self.right.insert(node)
        else:
            self.left = self.left.insert(node)
        return self

    def find(self, key: K) -> TreapNode[K]:
        if not self:
            raise KeyError(f"No such key: {key}")
        if self.key == key:
            return self
        if self.key < key:
            return self.right.find(key)
        return self.left.find(key)

    def delete(self, key: K) -> TreapNode[K]:
        if not self:
            raise KeyError(f"No such key: {key}")
        if self.key == key:
            return self.left.merge(self.right)
        if self.key < key:
            self.right = self.right.delete(key)
            return self
        self.left = self.left.delete(key)
        return self

    def walk_direct(self) -> Iterator[TreapNode[K]]:
        if not self:
            return
        yield self
        for node in self.left.walk_direct():
            yield node
        for node in self.right.walk_direct():
            yield node

    def merge(self, other: TreapNode[K]) -> TreapNode[K]:
        if not self:
            return other
        if not other:
            return self
        if self.y < other.y:
            other.left = self.merge(other.left)
            return other
        else:
            self.right = self.right.merge(other)
            return self

    def split(self, key: K) -> Tuple[TreapNode[K], TreapNode[K]]:
        if not self:
            return TreapNode.NIL_VERTEX, TreapNode.NIL_VERTEX
        if self.key < key:
            self.right, other = self.right.split(key)
            return self, other
        other, self.left = self.left.split(key)
        return other, self

    def to_dict(self) -> Dict[K, Any]:
        d = {}
        for node in self.walk_direct():
            d[node.key] = node.value
        return d


class Treap(Generic[K]):
    """
    Tree of Nodes: (x, y)
    by x - it is a binary tree, no duplicates
    by y - it is a max heap
    """

    def __init__(self, init_dict: Optional[Dict[K, Any]] = None):
        self.root: TreapNode = TreapNode.NIL_VERTEX
        if init_dict:
            for key, item in init_dict.items():
                self[key] = item

    def __repr__(self):
        return self.root.__repr__()

    def __eq__(self, other: Any):
        if not isinstance(other, Treap):
            return False
        return self.to_dict() == other.to_dict()

    def to_dict(self) -> Dict[K, Any]:
        return self.root.to_dict()

    def __iter__(self) -> Iterator[TreapNode[K]]:
        return self.root.walk_direct()

    def __getitem__(self, key: K) -> Any:
        return self.root.find(key).value

    def __setitem__(self, key: K, value: Any):
        try:
            self.root.find(key).value = value
        except KeyError:
            self.root = self.root.insert(TreapNode(key, value))

    def __contains__(self, key: K) -> bool:
        try:
            self.root.find(key)
            return True
        except KeyError:
            return False

    def __delitem__(self, key: K):
        self.root = self.root.delete(key)
