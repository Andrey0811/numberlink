from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Path:
    start: Optional[tuple]
    end: Optional[tuple]


@dataclass
class Segment:
    active: set
    passive: set = field(default_factory=set)

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
