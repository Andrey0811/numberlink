import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from numberlink.colors import MAX_COLORS
from numberlink.core.solver import Solver
from numberlink.gui.field_button import FieldButton
from numberlink.core.triangle_field import TriangleField


class TriangleBoard(QWidget):
    def __init__(self, field, parent):
        super().__init__(parent)
        self.solver = Solver()
        self._field = TriangleField(field)
        self.board_size = self._field.size
        self.cells = []
        self.cell_length = 50
        self.init_ui()
        self._current_number = 1
        self.targets = self._field.get_targets()['vertices']
        self.solutions = list(set(TriangleField(
            self.solver.get_field_from_solution(self._field, solution))
            for solution in self.solver.solve(self._field)))
        self.when_solved = lambda x: None

        for cell in self.cells:
            if cell.position in self.targets:
                cell.is_static = True

    def init_ui(self):
        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)

        for i, row in enumerate(self._field):
            hbox = QHBoxLayout(self)
            hbox.setAlignment(Qt.AlignCenter)

            for j, number in enumerate(row):
                cell = FieldButton(
                    (i, j),
                    self,
                    self.cell_length,
                    int(self.cell_length * 2 / 3)
                    if (j != 0 and j != len(row) - 1) and j % 2 != 0
                    else self.cell_length)
                cell.number = number
                cell.on_mouse_click = functools.partial(self.cell_click, cell)
                self.cells.append(cell)
                hbox.addWidget(cell, 0, Qt.AlignCenter)

            vbox.addLayout(hbox)
        self.setLayout(vbox)

    def cell_click(self, cell):
        if cell.position not in self.targets:
            self._field[cell.position] = cell.number
            if self.check_solution():
                self.when_solved('Головоломка решена!')

    def clear(self):
        for cell in self.cells:
            if cell.position not in self.targets:
                cell.number = 0
                self._field[cell.position] = 0

    def check_solution(self):
        return any(self._field == solution for solution in self.solutions)

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, field):
        for i, row in enumerate(field):
            for j, cell in enumerate(row):
                self._field[i, j] = cell
        for cell in self.cells:
            cell.number = self._field[cell.position]

    @property
    def current_number(self):
        return self._current_number

    @current_number.setter
    def current_number(self, value: int):
        if 0 < value < MAX_COLORS:
            self._current_number = value
