from typing import List

from graph_tools import Graph

CELL_EMPTY_VALUE = 0
MAX_NUMBER = 100


class TriangleField:
    def __init__(self, field):
        self.check_field(field)
        self._field = [list(map(int, row)) for row in field]

    def __setitem__(self, key, value):
        row, col = key
        self._field[row][col] = value

    def __getitem__(self, key):
        row, col = key
        return self._field[row][col]

    def __iter__(self):
        yield from self._field

    def __eq__(self, other):
        for i, row in enumerate(self._field):
            for j, cell in enumerate(row):
                if other[i, j] != self[i, j]:
                    return False
        return True

    def __str__(self):
        size = len(self._field)
        output_str = [(' ' * (size - i - 1))
                      + ''.join(map(str, self._field[i]))
                      for i in range(len(self._field))]
        return '\n'.join(map(str, output_str))

    def get_environment(self, row, col):
        directions = []

        if row > 0 and col % 2 != 0:
            directions.append((-1, -1))
        elif row + 1 < self.size and col % 2 == 0:
            directions.append((1, 1))
        if col > 0:
            directions.append((0, -1))
        if col + 1 < len(self._field[row]):
            directions.append((0, 1))

        for dy, dx in directions:
            yield row + dy, col + dx

    def get_neighbours(self, row, col):
        yield from (pos for pos in self.get_environment(row, col)
                    if self.is_valid(*pos))

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

    @staticmethod
    def check_field(field: List[List]):
        if (not isinstance(field, list)
                or (len(field) > 0 and not isinstance(field[0], list))):
            raise ValueError('Incorrect field')

        if len(field[0]) != 1:
            field = list(reversed(field))

        start = 1
        for i in field[1:]:
            start += 2

            if len(i) != start:
                raise ValueError('Incorrect field')

    def __hash__(self):
        result = ()
        for i in self._field:
            result = (result, tuple(i))
        return result.__hash__()