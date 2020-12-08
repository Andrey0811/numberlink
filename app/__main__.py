import sys

from PyQt5.QtWidgets import QApplication

from app.gui.main_windows import MainWindow

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        app.setStyle('Fusion')
        sys.exit(app.exec())
    except Exception as e:
        print(e.args[0])
        sys.exit(-1)
