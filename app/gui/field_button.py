from PyQt5.QtWidgets import QPushButton

from app.colors import MAX_COLORS, Color


class FieldButton(QPushButton):
    def __init__(self, position, parent, width, height):
        super().__init__('0', parent)
        self.position = position
        self.number = 0
        self.setMinimumSize(width, height)
        self._on_mouse_click = None

    @property
    def number(self):
        return int(self.text()) if self.text() else 0

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
        self.number = self.parent().current_number % MAX_COLORS
        if self.on_mouse_click:
            self.on_mouse_click()
        super().mousePressEvent(e)
