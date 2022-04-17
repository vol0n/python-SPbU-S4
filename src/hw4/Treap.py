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
    def __init__(
        self,
        key: K,
        value: Any,
        y: float = random.random(),
        left: Optional[TreapNode[K]] = None,
        right: Optional[TreapNode[K]] = None,
    ):
        self.key: K = key
        self.value: Any = value
        self.y: float = y
        self.right: Optional[TreapNode] = left
        self.left: Optional[TreapNode] = right

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TreapNode):
            return False
        return self.to_dict() == other.to_dict()

    def _print_tree(self) -> list[str]:
        node_repr = f"({self.key}, {self.value})"
        node_w = len(node_repr)

        left_repr = self.left._print_tree() if self.left else []
        left_w = len(left_repr[0]) if left_repr else 0
        left_h = len(left_repr)

        right_repr = self.right._print_tree() if self.right else []
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
        if self.key == node.key:
            return node
        if self.y < node.y:
            node.left, node.right = split(self, node.key)
            return node

        if self.key < node.key:
            if self.right:
                self.right = self.right.insert(node)
            else:
                self.right = node
        else:
            if self.left:
                self.left = self.left.insert(node)
            else:
                self.left = node
        return self

    def find(self, key: K) -> TreapNode[K]:
        if self.key == key:
            return self
        if self.key < key:
            if self.right:
                return self.right.find(key)
            raise KeyError(f"No such key: {key}")
        if self.left:
            return self.left.find(key)
        raise KeyError(f"No such key: {key}")

    def delete(self, key: K) -> Optional[TreapNode[K]]:
        """
        :param key: key of a node to delete
        :raises: KeyError if there is no node with key
        :return: this TreapNode without a node or None if resulting TreapNode is empty
        """
        if self.key == key:
            return merge(self.left, self.right)
        if self.key < key:
            if self.right:
                self.right = self.right.delete(key)
                return self
            raise KeyError(f"No such key: {key}")
        if self.left:
            self.left = self.left.delete(key)
            return self
        raise KeyError(f"No such key: {key}")

    def walk_direct(self) -> Iterator[TreapNode[K]]:
        yield self
        if self.left:
            for node in self.left.walk_direct():
                yield node
        if self.right:
            for node in self.right.walk_direct():
                yield node

    def to_dict(self) -> Dict[K, Any]:
        d = {}
        for node in self.walk_direct():
            d[node.key] = node.value
        return d


def merge(this: Optional[TreapNode[K]], other: Optional[TreapNode[K]]) -> Optional[TreapNode[K]]:
    if not this:
        return other
    if not other:
        return this
    if this.y < other.y:
        other.left = merge(this, other.left)
        return other
    else:
        this.right = merge(this.right, other)
        return this


def split(node: Optional[TreapNode[K]], key: K) -> Tuple[Optional[TreapNode[K]], Optional[TreapNode[K]]]:
    if not node:
        return None, None
    if node.key < key:
        node.right, other = split(node.right, key)
        return node, other
    other, node.left = split(node.left, key)
    return other, node


class Treap(Generic[K]):
    """
    Tree of Nodes: (x, y)
    by x - it is a binary tree, no duplicates
    by y - it is a max heap
    """

    def __init__(self, init_dict: Optional[Dict[K, Any]] = None):
        self.root: Optional[TreapNode[K]] = None
        if init_dict:
            for key, item in init_dict.items():
                self[key] = item

    def __repr__(self):
        return self.root.__repr__() if self.root else ""

    def __eq__(self, other: Any):
        if not isinstance(other, Treap):
            return False
        return self.to_dict() == other.to_dict()

    def to_dict(self) -> Dict[K, Any]:
        if not self.root:
            return {}
        return self.root.to_dict()

    def __iter__(self) -> Iterator[TreapNode[K]]:
        return self.root.walk_direct() if self.root else iter(())

    def __getitem__(self, key: K) -> Any:
        if self.root:
            return self.root.find(key).value
        raise KeyError(f"No such key: {key}")

    def __setitem__(self, key: K, value: Any):
        if not self.root:
            self.root = TreapNode(key, value)
            return
        try:
            self.root.find(key).value = value
        except KeyError:
            self.root = self.root.insert(TreapNode(key, value))

    def __contains__(self, key: K) -> bool:
        if not self.root:
            return False
        try:
            self.root.find(key)
            return True
        except KeyError:
            return False

    def __delitem__(self, key: K):
        if not self.root:
            raise KeyError(f"No such key: {key}")
        self.root = self.root.delete(key)
