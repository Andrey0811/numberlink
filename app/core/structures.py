from typing import List, Dict


class Path:
    def __init__(self, start: tuple = None, end: tuple = None):
        self.start = start
        self.end = end


class Segment:
    def __init__(self, iterable: list):
        self.active = set(iterable)
        self.passive = set()

    def leave(self, item):
        self.active.remove(item)
        self.passive.add(item)


class Node:
    first_second = None
    second_link = None

    def __init__(self, edge: List[tuple],
                 neighbors: Dict[tuple, tuple],
                 name: int):
        self.edge = edge
        self.neighbor = neighbors
        self.name = name
        self.first = None
        self.second = None

    def add_link(self, first_link, second_link):
        self.first = first_link
        self.second = second_link

    @property
    def links(self):
        return self.first, self.second


Node.second_link = Node(None, None, 1)
Node.first_second = Node(None, None, 0)
