
import sys
from PyQt6.QtWidgets import QApplication
from shell.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("styless.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
