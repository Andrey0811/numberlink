import random
from typing import List, Tuple

from app.const import DEFAULT_FIELD_HEIGHT, COUNT_NEIGHBORS
from app.numberlink import TriangleField, MAX_NUMBER, CELL_EMPTY_VALUE


class Path:
    def __init__(self, start: tuple = None, end: tuple = None):
        self.start = start
        self.end = end


class CreatorPath:
    def __init__(self, field: TriangleField):
        self.field = field
        self.covered_cells = 0
        self.cells_amount = self.count_cells(self.field.size)
        self.paths = []

    @property
    def number(self) -> int:
        return len(self.paths) + 1

    def count_busy_neighbours(self, pos: tuple) -> int:
        return count(point for point in self.field.get_environment(*pos)
                     if not self.field.is_valid(*point)
                     or self.field[point] != CELL_EMPTY_VALUE)

    def count_number_neighbours(self, pos: tuple, number: int) -> int:
        return count(point for point in self.field.get_neighbours(*pos)
                     if self.field[point] == number)

    def is_cycle(self, pos, number) -> bool:
        return self.count_number_neighbours(pos, number) > 1

    def is_isolated(self, pos: tuple, number: int, is_last: bool) -> bool:
        return (self.count_busy_neighbours(pos) == COUNT_NEIGHBORS
                and (not is_last or self.is_cycle(pos, number)))

    def has_isolated_empty_cells(self, pos: tuple,
                                 number: int,
                                 is_last: bool) -> bool:
        neighbours = self.field.get_neighbours(*pos)
        return any(
            self.is_isolated(place, number, is_last) for place in neighbours
            if self.field[place] == CELL_EMPTY_VALUE)

    def can_add_cell(self, pos: tuple, number: int) -> bool:
        self.field[pos] = number
        isolated = self.has_isolated_empty_cells(pos, number, True)
        self.field[pos] = CELL_EMPTY_VALUE

        return not isolated

    def get_path_extens_neighbours(self, pos: tuple, number: int) -> tuple:
        neighbours = list(self.field.get_neighbours(*pos))
        idx = random.randint(0, len(neighbours) - 1)

        if not self.has_isolated_empty_cells(pos, number, False):
            for pos in neighbours[idx:] + neighbours[:idx]:
                if (self.field[pos] == CELL_EMPTY_VALUE
                        and self.can_add_cell(pos, number)):
                    return pos

    def try_get_path_begin(self) -> Tuple[tuple, tuple]:
        empty_cells = get_empty_cells(self.field)

        if empty_cells:
            idx = random.randint(0, len(empty_cells) - 1)
            for start in empty_cells[idx:] + empty_cells[:idx]:
                if self.can_add_cell(start, self.number):
                    end = self.get_path_extens_neighbours(start, self.number)

                    if end is not None:
                        return start, end

    def add_path(self, start: tuple, end: tuple):
        self.paths.append(Path(start))
        self.field[start] = self.field[end] = self.number
        self.covered_cells += 2

        while True:
            start = end
            end = self.get_path_extens_neighbours(start, self.number)

            if (end is not None
                    and self.covered_cells < self.cells_amount):
                self.field[end] = self.number
                self.covered_cells += 1
            else:
                self.paths[-1].end = start
                return

    def get_gaming_field(self) -> List[List]:
        field = generate_triangle_field(self.field.size)
        for i, path in enumerate(self.paths):
            for row, col in [path.start, path.end]:
                field[row][col] = i + 1

        return field

    def create(self) -> List[List]:
        while True:
            pair = self.try_get_path_begin()

            if pair is not None:
                self.add_path(*pair)
            elif (self.covered_cells >= self.cells_amount
                  and self.number <= MAX_NUMBER):
                return self.get_gaming_field()
            else:
                field = generate_triangle_field(self.field.size)
                self.__init__(TriangleField(field))

    @staticmethod
    def count_cells(size: int) -> int:
        count_cells = 0
        for i in range(size):
            count_cells += i * 2 + 1

        return count_cells


def count(iterable) -> int:
    return sum(1 for _ in iterable)


def get_empty_cells(field: TriangleField) -> List[tuple]:
    result = []
    for i, row in enumerate(field.field):
        for j, cell in enumerate(row):
            if cell == CELL_EMPTY_VALUE:
                result.append((i, j))

    return result


def generate_triangle_field(size: int) -> List[List]:
    field = [[0]]
    for i in range(1, size):
        field.append([0 for _ in range(i * 2 + 1)])

    return field


def generate_field(size: int = 3):
    size = max(DEFAULT_FIELD_HEIGHT, size)
    field = generate_triangle_field(size)
    constructor = CreatorPath(TriangleField(field))

    return constructor.create()
