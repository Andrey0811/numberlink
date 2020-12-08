from typing import List

from graph_tools import Graph

CELL_EMPTY_VALUE = 0
MAX_NUMBER = 100


class TriangleField:
    def __init__(self, field):
        # self._check_hexagonal(field)
        self._field = [list(map(int, level)) for level in field]

    def __setitem__(self, key, value):
        level, index = key
        self._field[level][index] = value

    def __getitem__(self, key):
        level, index = key
        return self._field[level][index]

    def __iter__(self):
        yield from self._field

    def __eq__(self, other):
        for i, level in enumerate(self._field):
            for j, cell in enumerate(level):
                if other[i, j] != self[i, j]:
                    return False
        return True

    def get_environment(self, level, idx):
        directions = []

        if level > 0 and idx % 2 != 0:
            directions.append((-1, -1))
        elif level + 1 < self.size and idx % 2 == 0:
            directions.append((1, 1))
        if idx > 0:
            directions.append((0, -1))
        if idx + 1 < len(self._field[level]):
            directions.append((0, 1))

        for dy, dx in directions:
            yield level + dy, idx + dx

    def get_neighbours(self, level, index):
        yield from (position for position in self.get_environment(level, index)
                    if self.is_valid(*position))

    @property
    def field(self) -> List[List]:
        return self._field

    @property
    def size(self):
        return len(self._field)

    def is_valid(self, level, key):
        return (0 <= level < len(self._field)
                and 0 <= key < len(self._field[level]))

    def make_graph(self):
        graph = Graph(directed=False, multiedged=False)

        for i, level in enumerate(self._field):
            for j, cell, in enumerate(level):
                start = i, j
                ends = [i for i in self.get_environment(i, j)]

                for valid_end in (end for end in ends if self.is_valid(*end)):
                    graph.add_edge(start, valid_end)

        return graph

    def get_targets(self):
        targets = dict(vertices=set(), pairs=set())
        pairs = {}

        for i, row in enumerate(self._field):
            for j, cell in enumerate(row):
                if cell is not CELL_EMPTY_VALUE:
                    if cell in pairs:
                        targets["pairs"].add(frozenset((pairs[cell], (i, j))))
                    else:
                        pairs[cell] = (i, j)
                    targets["vertices"].add((i, j))

        return targets
