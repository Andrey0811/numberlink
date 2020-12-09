import sys

from PyQt5.QtWidgets import QApplication

from numberlink.gui.main_windows import MainWindow


app = QApplication(sys.argv)
window = MainWindow()
app.setStyle('Fusion')
sys.exit(app.exec())
