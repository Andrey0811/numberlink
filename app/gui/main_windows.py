import sys

from PyQt5.QtWidgets import (QMainWindow,
                             QStackedWidget, QFileDialog)

from app import reader
from app.const import TITLE, \
    START_MAIN_WINDOW, SIZE_MAIN_WINDOW
from app.core.generator import generate_field
from app.gui.game_window import GameWindow
from app.gui.menu import Menu


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
