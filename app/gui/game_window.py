import random
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QPushButton, QHBoxLayout, \
    QVBoxLayout, QLabel, QDialog, QLineEdit, QWidget

from app.const import TITLE
from app.gui.triangle_board import TriangleBoard


class GameWindow(QWidget):
    def __init__(self, field: List[List], parent):
        super().__init__(parent)
        self.board = TriangleBoard(field, self)
        self.init_ui()

    def init_ui(self):
        solve_btn = QPushButton('Решение', self)
        solve_btn.clicked.connect(self.solve)

        menu_btn = QPushButton('Меню', self)
        menu_btn.clicked.connect(self.window().menu)

        clear_btn = QPushButton('Очистить', self)
        clear_btn.clicked.connect(self.clear)

        self.number_label = QLabel(f'Текущее число: '
                                   f'{str(self.board.current_number)}', self)
        self.number_editor = QLineEdit(str(self.board.current_number), self)
        number_btn = QPushButton('Ввод', self)
        number_btn.clicked.connect(self.window().click_number_change)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addWidget(solve_btn, 0, Qt.AlignCenter)
        hbox.addWidget(clear_btn, 0, Qt.AlignCenter)
        hbox.addWidget(menu_btn, 0, Qt.AlignCenter)
        hbox.addWidget(self.number_label, 1, Qt.AlignCenter)
        hbox.addWidget(self.number_editor, 2, Qt.AlignCenter)
        hbox.addWidget(number_btn, 2, Qt.AlignCenter)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.board, 0, Qt.AlignCenter)
        vbox.addLayout(hbox)

        self.board.when_solved = self.show_finish_dialog

    def show_finish_dialog(self):
        msb = QDialog(self)
        msb.resize(100, 100)
        msb.setWindowTitle(TITLE)
        msb.show()

        text = QLabel()
        text.setText('Вы решили задачу')

        return_btn = QPushButton('Вернуться', msb)
        return_btn.clicked.connect(msb.close)

        menu_btn = QPushButton('Меню', msb)
        menu_btn.clicked.connect(self.window().menu)
        menu_btn.clicked.connect(msb.close)

        hbox = QHBoxLayout(self)
        hbox.addWidget(return_btn, 0, Qt.AlignCenter)
        hbox.addWidget(menu_btn, 0, Qt.AlignCenter)

        vbox = QVBoxLayout(msb)
        vbox.addWidget(text, 0, Qt.AlignCenter)
        vbox.addLayout(hbox)

    def solve(self):
        if not self.board.solutions:
            self.show_no_solutions()
        else:
            index = random.randint(0, len(self.board.solutions) - 1)
            self.board.set_field(self.board.solutions[index].field)

    @staticmethod
    def show_no_solutions():
        msg = QMessageBox()
        msg.setWindowTitle(TITLE)
        msg.setIcon(QMessageBox.Information)
        msg.setText('К сожалению, решений нет')
        msg.show()

    def clear(self):
        self.board.clear()
