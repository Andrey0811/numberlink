import random
import sys
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QVBoxLayout, QHBoxLayout,
                             QMessageBox, QDialog,
                             QLabel, QMainWindow,
                             QStackedWidget, QLineEdit,
                             QFileDialog)

from app import reader
from app.algorithms.generator import generate_field
from app.const import DEFAULT_FIELD_HEIGHT, TITLE, \
    START_MAIN_WINDOW, SIZE_MAIN_WINDOW
from app.gui.board import GameBoard


class Menu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        load_game_btn = QPushButton('Загрузить игру', self)
        load_game_btn.clicked.connect(self.window().load_game_from_file)

        exit_btn = QPushButton('Выход', self)
        exit_btn.clicked.connect(self.window().exit)

        size_label = QLabel('Размер доски', self)
        self.size_editor = QLineEdit(str(DEFAULT_FIELD_HEIGHT), self)

        generate_btn = QPushButton('Сгенерировать уровень', self)
        generate_btn.clicked.connect(self.window().generate_level)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)

        if reader.exist_save_field():
            continue_game_button = QPushButton('Продолжить игру', self)
            continue_game_button.clicked.connect(
                self.window().load_game_from_save)
            vbox.addWidget(continue_game_button, 0, Qt.AlignCenter)

        vbox.addWidget(load_game_btn, 0, Qt.AlignCenter)
        vbox.addWidget(size_label, 0, Qt.AlignCenter)
        vbox.addWidget(self.size_editor, 0, Qt.AlignCenter)
        vbox.addWidget(generate_btn, 0, Qt.AlignCenter)
        vbox.addWidget(exit_btn, 0, Qt.AlignCenter)


class GameWindow(QWidget):
    def __init__(self, field: List[List], parent):
        super().__init__(parent)
        self.board = GameBoard(field, self)
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

    def show_no_solutions(self):
        msg = QMessageBox()
        msg.setWindowTitle(TITLE)
        msg.setIcon(QMessageBox.Information)
        msg.setText('К сожалению, решений нет')
        msg.show()

    def clear(self):
        self.board.clear()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_menu = Menu(self)
        self.game = None
        self.history = []
        self.init_ui()

    def init_ui(self):
        self.setGeometry(*START_MAIN_WINDOW,
                         *SIZE_MAIN_WINDOW)
        self.show()
        self.setWindowTitle(TITLE)

        stacked_widget = QStackedWidget(self)
        self.setCentralWidget(stacked_widget)
        self.centralWidget().addWidget(self.main_menu)
        self.menu()

    def menu(self):
        self.history.clear()
        self.centralWidget().setCurrentWidget(self.main_menu)

    def generate_level(self):
        self.history.clear()
        size = self.main_menu.size_editor.text()
        self.game = GameWindow(generate_field(int(size)), self)
        self.centralWidget().addWidget(self.game)
        self.centralWidget().setCurrentWidget(self.game)

    def load_game(self, field):
        self.history.clear()
        self.game = GameWindow(field, self)
        self.centralWidget().addWidget(self.game)
        self.centralWidget().setCurrentWidget(self.game)

    def go_back(self):
        self.centralWidget().setCurrentWidget(self.history.pop())

    def exit(self):
        self.close()

    def load_game_from_file(self):
        self.history.clear()
        filename, filetype = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', '.', 'Text Files(*.txt);;All Files(*)')
        if filename == '':
            self.menu()
        else:
            field = reader.get_field_from_file(filename)
            self.load_game(field)

    def load_game_from_save(self):
        self.history.clear()
        self.load_game(reader.get_field_from_save())

    def closeEvent(self, event):
        reader.save_list_of_field(self.game.board.field)
        sys.exit(0)

    def click_number_change(self):
        text = self.game.number_editor.text()
        try:
            self.game.board.current_number = int(text)
            self.game.number_editor.setText(str(
                self.game.board.current_number))
            self.set_text_label(self.game.number_label,
                                f'Текущее число: '
                                f'{str(self.game.board.current_number)}')
        except Exception as e:
            print(e.args)

    @staticmethod
    def set_text_label(label, text):
        label.setText(text)
        label.adjustSize()
