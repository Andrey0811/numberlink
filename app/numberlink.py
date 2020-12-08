import collections
import itertools
import copy
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

    # @staticmethod
    # def _check_hexagonal(field):
    #     size = {
    #         "vertical": len(field),
    #         "horizontal": max(len(level) for level in field)
    #     }
    #     if size["vertical"] != size["horizontal"] or size["vertical"] % 2 == 0:
    #         raise ValueError(
    #             f"Некорректные размеры поля: "
    #             f"{size['horizontal']} x {size['vertical']}")
    #     middle = len(field) // 2
    #     for i in range(middle):
    #         if len(field[middle - i - 1]) != len(field) - i - 1:
    #             raise ValueError(f"Неверная длина {i - 1}-го уровня.")
    #         if len(field[middle + i + 1]) != len(field) - i - 1:
    #             raise ValueError(f"Неверная длина {i + 1}-го уровня.")

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


class TriangleLink(TriangleField):

    def __init__(self, field: List[List]):
        # HexLink.check_field(field)
        super().__init__(field)

    def __getitem__(self, key):
        level, index = key
        return self._field[level][index]

    def __setitem__(self, key, value):
        level, index = key
        self._field[level][index] = value

    def get_targets(self):
        targets = {"vertices": set(), "pairs": set()}
        pairs = {}

        for i, level in enumerate(self._field):
            for j, cell in enumerate(level):
                if cell is not CELL_EMPTY_VALUE:
                    if cell in pairs:
                        targets["pairs"].add(frozenset((pairs[cell], (i, j))))
                    else:
                        pairs[cell] = (i, j)
                    targets["vertices"].add((i, j))

        return targets

    # @staticmethod
    # def check_field(field):
    #     if field is None:
    #         raise ValueError("Поле было None.")
    #     TriangleLink._check_cells(field)
    #     TriangleLink._check_pairs(field)
    #     TriangleLink._check_range(field)
    #     TriangleLink._check_order(field)
    #
    # @staticmethod
    # def _check_pairs(field):
    #     items = collections.Counter(map(str, itertools.chain(*field)))
    #     del items[str(CELL_EMPTY_VALUE)]
    #     if not items:
    #         raise ValueError("Не обнаружено пар чисел.")
    #     filtered = [number for number, repeat in items.items() if repeat != 2]
    #     if filtered:
    #         raise ValueError(
    #             f"Некорректное количество чисел: {', '.join(filtered)}"
    #         )
    #
    # @staticmethod
    # def _check_range(field):
    #     for number in map(int, itertools.chain(*field)):
    #         if number > MAX_NUMBER:
    #             raise ValueError(
    #                 f"Числа не могут превышать: {MAX_NUMBER}."
    #                 f" Было получено: {number}"
    #             )
    #         if number < CELL_EMPTY_VALUE:
    #             raise ValueError(
    #                 f"Числа не могут быть отрицательными."
    #                 f" Было получено: {number}"
    #             )
    #
    # @staticmethod
    # def _check_order(field):
    #     items = {*map(int, itertools.chain(*field))}
    #     failed = [i for i in range(max(*items) + 1) if i not in items]
    #     if failed:
    #         raise ValueError(
    #                 f"Нарушен порядок следования. "
    #                 f"Не обнаружено: {', '.join(map(str, failed))}"
    #         )
    #
    # @staticmethod
    # def _check_cells(field):
    #     for i, level in enumerate(field):
    #         for j, cell in enumerate(level):
    #             if not str(cell).isnumeric():
    #                 raise ValueError(f"Некорректный символ на позиции {i, j}")
