from PyQt6.QtWidgets import QApplication
import sys
import database
from ui_start import StartWindow

if __name__ == "__main__":
    database.init_db()
    app = QApplication(sys.argv)
    start = StartWindow()
    start.show()
    sys.exit(app.exec())
