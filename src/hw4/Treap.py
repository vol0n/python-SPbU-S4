from typing import Optional, Tuple


class TreapNode:
    def __init__(self, x, y, left: Optional["TreapNode"] = None, right: Optional["TreapNode"] = None):
        self.x = x
        self.y = y
        self.right: Optional["TreapNode"] = right
        self.left: Optional["TreapNode"] = left

    def __eq__(self, other):
        if not isinstance(other, TreapNode):
            return False
        return self.x == other.x and self.y == other.y and self.left == other.left and self.right == other.right


    @staticmethod
    def from_list(nodes):
        def add(i):
            if i < len(nodes):
                if not nodes[i]:
                    return None
                return TreapNode(*nodes[i], add(2 * i + 1), add(2 * i + 2))
            return None

        return add(0)

    @staticmethod
    def merge(fst: Optional["TreapNode"], snd: Optional["TreapNode"]):
        if not fst:
            return snd
        if not snd:
            return fst
        if fst.y < snd.y:
            snd.left = TreapNode.merge(fst, snd.left)
            return snd
        else:
            fst.right = TreapNode.merge(fst.right, snd)
            return fst

    @staticmethod
    def split(treap: Optional["TreapNode"], key) -> Tuple[Optional["TreapNode"], ...]:
        if not treap:
            return None, None
        if treap.x < key:
            treap.right, other = TreapNode.split(treap.right, key)
            return treap, other
        other, treap.left = TreapNode.split(treap.left, key)
        return other, treap

    @staticmethod
    def print_tree(node):
        if not node:
            return []

        node_repr = f"({node.x}, {node.y})"
        node_len = len(node_repr)

        left_repr = TreapNode.print_tree(node.left)
        left_w = len(left_repr[0]) if left_repr else 0
        left_h = len(left_repr)

        right_repr = TreapNode.print_tree(node.right)
        right_w = len(right_repr[0]) if right_repr else 0
        right_h = len(right_repr)

        new_repr = [
            " " * (left_w - left_w // 2)
            + "_" * (left_w // 2)
            + node_repr
            + "_" * (right_w // 2)
            + " " * (right_w - right_w // 2)
        ]
        w = left_w + right_w + node_len
        if node.left or node.right:
            second_line = [" "] * w
            if node.left:
                second_line[left_w - left_w // 2] = "|"
            if node.right:
                second_line[w - right_w + right_w // 2 - 1] = "|"
            new_repr.append("".join(second_line))

        i = 0
        while i < left_h and i < right_h:
            new_repr.append(left_repr[i] + " " * node_len + right_repr[i])
            i += 1
        while i < left_h:
            new_repr.append(left_repr[i] + " " * (node_len + right_w))
        while i < right_h:
            new_repr.append(" " * (node_len + left_w) + right_repr[i])
            i += 1
        return new_repr

    def __repr__(self):
        return "\n".join(TreapNode.print_tree(self))

    @staticmethod
    def insert(treap: Optional["TreapNode"], node: "TreapNode"):
        if not treap or treap.x == node.x:
            return node
        if treap.y < node.y:
            node.left, node.right = TreapNode.split(treap, node.x)
            return node
        if treap.x < node.x:
            treap.right = TreapNode.insert(treap.right, node)
        else:
            treap.left = TreapNode.insert(treap.left, node)
        return treap

    @staticmethod
    def find(node: Optional["TreapNode"], x):
        if not node:
            raise KeyError
        if node.x == x:
            return node
        if node.x < x:
            return TreapNode.find(node.right, x)
        return TreapNode.find(node.left, x)

    @staticmethod
    def delete(node: Optional["TreapNode"], key):
        if not node:
            raise KeyError(f"No such key: {key}")
        if node.x == key:
            return TreapNode.merge(node.left, node.right)
        if node.x < key:
            node.right = TreapNode.delete(node.right, key)
            return node
        node.left = TreapNode.delete(node.left, key)
        return node

    @staticmethod
    def walk_direct(node: Optional["TreapNode"]):
        if not node:
            return
        yield node
        for v in TreapNode.walk_direct(node.left):
            yield v
        for v in TreapNode.walk_direct(node.right):
            yield v


class Treap:
    """
    Tree of Nodes: (x, y)
    by x - it is a binary tree, no duplicates
    by y - it is a max heap
    """

    def __init__(self, init_dict: Optional[dict] = None):
        self.root: Optional[TreapNode] = None
        if init_dict:
            for key, item in init_dict.items():
                self.root = TreapNode.insert(self.root, TreapNode(key, item))

    def __repr__(self):
        return self.root.__repr__()

    def __eq__(self, other):
        if not isinstance(other, Treap):
            return False
        return self.to_dict() == other.to_dict()

    def to_dict(self):
        d = {}
        for node in self:
            d[node.x] = node.y
        return d

    def __iter__(self):
        return TreapNode.walk_direct(self.root)

    def __getitem__(self, item):
        return TreapNode.find(self.root, item).y

    def __setitem__(self, key, value):
        try:
            TreapNode.find(self.root, key).y = value
        except KeyError:
            self.root = TreapNode.insert(self.root, TreapNode(key, value))

    def __contains__(self, item):
        try:
            TreapNode.find(self.root, item)
            return True
        except KeyError:
            return False

    def __delitem__(self, key):
        self.root = TreapNode.delete(self.root, key)

    @staticmethod
    def from_list(nodes: list):
        """
        This func is for quickly creating test treaps.
        """
        t = Treap()
        t.root = TreapNode.from_list(nodes)
        return t
