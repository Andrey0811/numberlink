from typing import List, Dict


class Segment:
    def __init__(self, iterable: list):
        self.active = set(iterable)
        self.thrown = set()

    def throw(self, item):
        self.active.remove(item)
        self.thrown.add(item)


class Node:
    link_zero = None
    link_one = None

    def __init__(self, edge: List[tuple],
                 neighbors: Dict[tuple, tuple],
                 name: int):
        self.edge = edge
        self.neighbor = neighbors
        self.name = name
        self.zero_child = None
        self.one_child = None

    def add_children(self, zero_child, one_child):
        self.zero_child = zero_child
        self.one_child = one_child

    @property
    def children(self):
        return self.zero_child, self.one_child


Node.link_one = Node(None, None, 1)
Node.link_zero = Node(None, None, 0)
