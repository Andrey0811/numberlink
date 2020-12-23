import random
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, \
    QVBoxLayout, QLabel, QDialog, QLineEdit, QWidget

from numberlink_puzzle.const import TITLE, SIZE_DIALOG_WINDOW
from numberlink_puzzle.gui.triangle_board import TriangleBoard


class GameWindow(QWidget):
    def __init__(self, field: List[List], parent):
        super().__init__(parent)
        self.board = TriangleBoard(field, self)
        self.init_ui()

    def init_ui(self):
        solve_btn = QPushButton('Решение', self)
        solve_btn.clicked.connect(self.solve)

        menu_btn = QPushButton('Меню', self)
        menu_btn.clicked.connect(self.window().go_to_menu)

        clear_btn = QPushButton('Очистить', self)
        clear_btn.clicked.connect(self.clear)

        self.number_label = QLabel(f'Текущее число: '
                                   f'{str(self.board.current_number)}', self)
        self.number_editor = QLineEdit(str(self.board.current_number), self)
        number_btn = QPushButton('Ввод', self)
        number_btn.clicked.connect(self.click_number_change)

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

        self.board.when_solved = self.show_dialog_message

    def show_dialog_message(self, message):
        msg = QDialog(self)
        msg.resize(*SIZE_DIALOG_WINDOW)
        msg.setWindowTitle(TITLE)

        text = QLabel(msg)
        text.setText(message)

        hbox = QHBoxLayout(msg)
        hbox.addWidget(text, 0, Qt.AlignCenter)
        msg.show()

    def solve(self):
        if not self.board.solutions:
            self.show_dialog_message('Решений нет')
        else:
            index = random.randint(0, len(self.board.solutions) - 1)
            self.board.field = self.board.solutions[index].field

    def clear(self):
        self.board.clear()

    def click_number_change(self):
        text = self.number_editor.text()
        try:
            self.board.current_number = int(text)
            self.number_editor.setText(str(
                self.board.current_number))
            self.set_text_label(self.game.number_label,
                                f'Текущее число: '
                                f'{str(self.game.board.current_number)}')
        except Exception as e:
            print(e.args)

    @staticmethod
    def set_text_label(label, text):
        label.setText(text)
        label.adjustSize()
