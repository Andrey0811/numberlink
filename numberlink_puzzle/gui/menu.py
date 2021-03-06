from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, \
    QLabel, QLineEdit, QVBoxLayout

from numberlink_puzzle.const import DEFAULT_FIELD_HEIGHT


class Menu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        load_game_btn = QPushButton('Загрузить игру', self)
        load_game_btn.clicked.connect(self.window().load_game_from_file)

        exit_btn = QPushButton('Выход', self)
        exit_btn.clicked.connect(self.window().close)

        size_label = QLabel('Размер доски', self)
        self.size_editor = QLineEdit(str(DEFAULT_FIELD_HEIGHT), self)

        generate_btn = QPushButton('Сгенерировать уровень', self)
        generate_btn.clicked.connect(self.window().generate_level)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)

        if self.parent().reader.exist_save_field():
            continue_game_btn = QPushButton('Продолжить игру', self)
            continue_game_btn.clicked.connect(
                self.window().load_game_from_save)
            vbox.addWidget(continue_game_btn, 0, Qt.AlignCenter)

        vbox.addWidget(load_game_btn, 0, Qt.AlignCenter)
        vbox.addWidget(size_label, 0, Qt.AlignCenter)
        vbox.addWidget(self.size_editor, 0, Qt.AlignCenter)
        vbox.addWidget(generate_btn, 0, Qt.AlignCenter)
        vbox.addWidget(exit_btn, 0, Qt.AlignCenter)
