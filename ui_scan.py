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
        self.back_btn = QPushButton("⬅️ Zurück")
        self.back_btn.clicked.connect(self.back)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("🔍 Scannen Sie den Barcode eines Artikels"))
        layout.addWidget(self.scan_input)
        layout.addWidget(self.output_box)
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

    def lookup(self):
        code = self.scan_input.text().strip()
        print(f"[DEBUG] Scanned code raw: {repr(code)}")
        item = database.get_product_by_code(code)
        self.scan_input.clear()
        if not item:
            QMessageBox.warning(self, "Nicht gefunden", "Kein Produkt mit diesem Code.")
            return
        text = (
            f"Code: {item[1]}\n"
            f"Gemeinde/VG: {item[2]}\n"
            f"Einsatzort: {item[3]}\n"
            f"Kategorie: {item[4]}\n"
            f"Produkttyp: {item[5]}\n"
            f"Produktdetails: {item[6]}\n"
            f"Anzahl: {item[7]}\n"
            f"Hersteller: {item[8]}\n"
            f"Lieferant: {item[9]}\n"
            f"Shop Link: {item[10]}\n" 
            f"Preis (Netto): {item[11] or ''}\n"
            f"Preis (Brutto): {item[12] or ''}\n"
            f"Bezahlt: {item[13]}\n"
            f"Bestellt am: {item[14]}\n"
            f"Geliefert am: {item[15]}\n"
            f"Übergeben am: {item[16]}\n"
            f"Projekt: {item[17]}\n"
            f"Bemerkungen: {item[18] or ''}"
        )
        self.output_box.setPlainText(text)


    def back(self):
        self.close()
        self.back_to_menu_requested.emit()




##Quickfix - US Keyboard
import unicodedata
def normalize_scanned_code(text: str) -> str:
    text = text.strip().replace("\r", "").replace("\n", "")
    text = unicodedata.normalize("NFKC", text)
    # Replace ß or other layout errors with '-'
    text = text.replace("ß", "-").replace("–", "-").replace("_", "-")
    return text