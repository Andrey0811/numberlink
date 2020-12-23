import sys

from PyQt5.QtWidgets import (QMainWindow,
                             QStackedWidget, QFileDialog)

from numberlink_puzzle.core.generator import Generator
from numberlink_puzzle.reader import Reader
from numberlink_puzzle.const import TITLE, \
    START_MAIN_WINDOW, SIZE_MAIN_WINDOW
from numberlink_puzzle.gui.game_window import GameWindow
from numberlink_puzzle.gui.menu import Menu


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.reader = Reader(Reader.get_resources_path())
        self.menu = Menu(self)
        self.game = None
        self.init_ui()

    def init_ui(self):
        self.setGeometry(*START_MAIN_WINDOW,
                         *SIZE_MAIN_WINDOW)
        self.show()
        self.setWindowTitle(TITLE)
        stacked_widget = QStackedWidget(self)
        self.setCentralWidget(stacked_widget)
        self.centralWidget().addWidget(self.menu)
        self.go_to_menu()

    def go_to_menu(self):
        if self.game:
            self.reader.save_list_of_field(self.game.board.field)
        self.centralWidget().setCurrentWidget(self.menu)

    def closeEvent(self, event):
        self.reader.save_list_of_field(self.game.board.field)
        sys.exit(0)

    def generate_level(self):
        size = self.menu.size_editor.text()
        self.create_game(Generator.generate_field(int(size)))

    def load_game(self, field):
        self.create_game(field)

    def load_game_from_file(self):
        filename, filetype = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', '.', 'Text Files(*.txt);;All Files(*)')
        if filename == '':
            self.go_to_menu()
        else:
            field = self.reader.get_field_from_file(filename)
            self.load_game(field)

    def load_game_from_save(self):
        self.load_game(self.reader.get_field_from_save())

    def create_game(self, field):
        self.game = GameWindow(field, self)
        self.centralWidget().addWidget(self.game)
        self.centralWidget().setCurrentWidget(self.game)
