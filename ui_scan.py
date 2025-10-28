from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
import database

class ScanWindow(QWidget):
    back_to_menu_requested = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lesemodus – Scannen")
        self.setMinimumWidth(500)

        self.parent = parent

        self.scan_input = QLineEdit()
        self.scan_input.setPlaceholderText("Code scannen...")
        self.scan_input.returnPressed.connect(self.lookup)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.back_btn = QPushButton("⬅️ Zurück zum Hauptmenü")
        self.back_btn.clicked.connect(self.back)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("🔍 Scannen Sie den Barcode eines Artikels"))
        layout.addWidget(self.scan_input)
        layout.addWidget(self.output_box)
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

    def lookup(self):
        code = self.scan_input.text().strip()
        item = database.get_product_by_code(code)
        self.scan_input.clear()
        if not item:
            QMessageBox.warning(self, "Nicht gefunden", "Kein Produkt mit diesem Code.")
            return
        text = (
            f"Name: {item[1]}\n"
            f"Code: {item[2]}\n"
            f"Kaufdatum: {item[3]}\n"
            f"Zugewiesen an: {item[4]}\n"
            f"Teilprojekt: {item[5]}\n"
            f"Lagerort: {item[6]}\n"
            f"Wert (€): {item[7]}\n"
            f"Bemerkungen: {item[8]}"
        )
        self.output_box.setPlainText(text)

    def back(self):
        self.close()
        self.back_to_menu_requested.emit()

