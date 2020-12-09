from PyQt5.QtWidgets import QPushButton

from numberlink.colors import MAX_COLORS, Color


class FieldButton(QPushButton):
    def __init__(self, position, parent, width, height):
        super().__init__('0', parent)
        self.position = position
        self.number = 0
        self.setMinimumSize(width, height)
        self._on_mouse_click = None
        self._is_static = False

    @property
    def number(self):
        return int(self.text()) if self.text() else 0

    @property
    def is_static(self):
        return self._is_static

    @is_static.setter
    def is_static(self, value: bool):
        self._is_static = value

    @property
    def on_mouse_click(self):
        return self._on_mouse_click

    @on_mouse_click.setter
    def on_mouse_click(self, value):
        self._on_mouse_click = value

    @number.setter
    def number(self, value):
        if value > MAX_COLORS:
            raise ValueError(f'Not supported count '
                             f'color more than {MAX_COLORS}')
        self.setText(str(value) if value > 0 else '0')
        self.setStyleSheet(
            f'QPushButton {{ background-color: {Color(value).name};}}')

    def mousePressEvent(self, e):
        if self._is_static:
            game_window = self.parent().parent()
            game_window.number_editor.setText(str(self.number))
            game_window.set_text_label(game_window.number_label, str(self.number))
            self.parent().current_number = self.number
        else:
            self.number = self.parent().current_number % MAX_COLORS
            if self.on_mouse_click:
                self.on_mouse_click()
            super().mousePressEvent(e)
