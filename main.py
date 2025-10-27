from PyQt6.QtWidgets import QApplication
import sys
import database
from ui_main import InventoryApp

if __name__ == "__main__":
    database.init_db()
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
