from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QListWidget, QDateEdit
)
from PyQt6.QtCore import QDate
import database
import barcode_utils
import utils
import export_utils

class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Land-lieben Inventar System")
        self.setMinimumWidth(600)

        # --- Inputs
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Produktname (z.B. Laptop HP)")

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Code (leer lassen für Auto)")

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Gemeinde-VG Kürzel (z.B. ALB)")

        self.purchase_date = QDateEdit()
        self.purchase_date.setCalendarPopup(True)
        self.purchase_date.setDate(QDate.currentDate())

        self.assigned_input = QLineEdit()
        self.assigned_input.setPlaceholderText("Zugewiesen an (Person oder Gemeinde)")

        self.subproject_input = QLineEdit()
        self.subproject_input.setPlaceholderText("Teilprojekt (ÖkoHaSie, Landlieben...)")

        self.storage_input = QLineEdit()
        self.storage_input.setPlaceholderText("Lagerort")

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Wert in €")

        self.remarks_input = QTextEdit()
        self.remarks_input.setPlaceholderText("Bemerkungen...")

        self.add_button = QPushButton("Hinzufügen")
        self.scan_input = QLineEdit()
        self.scan_input.setPlaceholderText("Code scannen...")

        self.export_btn = QPushButton("Exportieren (CSV)")
        self.export_btn.clicked.connect(self.export_csv)

        self.products_list = QListWidget()

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📦 Neues Produkt hinzufügen"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.code_input)
        layout.addWidget(self.location_input)
        layout.addWidget(QLabel("Kaufdatum:"))
        layout.addWidget(self.purchase_date)
        layout.addWidget(self.assigned_input)
        layout.addWidget(self.subproject_input)
        layout.addWidget(self.storage_input)
        layout.addWidget(self.value_input)
        layout.addWidget(self.remarks_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.export_btn)

        layout.addSpacing(10)
        layout.addWidget(QLabel("🔍 Produktinformation anzeigen"))
        layout.addWidget(self.scan_input)
        layout.addWidget(self.products_list)
        self.setLayout(layout)

        # Connections
        self.add_button.clicked.connect(self.add_product)
        self.scan_input.returnPressed.connect(self.lookup_product)

        # Init
        self.refresh_list()

    def add_product(self):
        name = self.name_input.text().strip()
        loc = self.location_input.text().strip().upper()
        manual_code = self.code_input.text().strip()
        code = manual_code or utils.generate_code(loc)

        purchase_date = self.purchase_date.date().toString("yyyy-MM-dd")
        assigned = self.assigned_input.text().strip()
        subproject = self.subproject_input.text().strip()
        storage = self.storage_input.text().strip()
        try:
            value = float(self.value_input.text().strip()) if self.value_input.text().strip() else None
        except ValueError:
            QMessageBox.warning(self, "Fehler", "Ungültiger Zahlenwert für 'Wert (€)'.")
            return
        remarks = self.remarks_input.toPlainText().strip()

        if not name or not loc:
            QMessageBox.warning(self, "Fehler", "Produktname und Kürzel sind erforderlich.")
            return

        import traceback

        try:
            database.add_product_safe(
                name=name,
                code=code,
                purchase_date=purchase_date,
                assigned_to=assigned,
                sub_project=subproject,
                storage_location=storage,
                value=value,
                remarks=remarks
            )
            label_text = f"Land-lieben: {assigned} - {subproject}"
            barcode_utils.generate_barcode(code, label_text)
            QMessageBox.information(self, "Erfolgreich", f"{name} hinzugefügt.\nCode: {code}")
            self.clear_inputs()
            self.refresh_list()

        except Exception as e:
            print("\n===== ERROR TRACEBACK =====")
            traceback.print_exc()
            print("============================\n")
            QMessageBox.warning(self, "Fehler", f"{type(e).__name__}: {e}")


    def lookup_product(self):
        code = self.scan_input.text().strip()
        item = database.get_product_by_code(code)
        self.scan_input.clear()
        if not item:
            QMessageBox.warning(self, "Nicht gefunden", "Kein Produkt mit diesem Code.")
            return
        info = (
            f"Name: {item[1]}\n"
            f"Code: {item[2]}\n"
            f"Kaufdatum: {item[3]}\n"
            f"Zugewiesen an: {item[4]}\n"
            f"Teilprojekt: {item[5]}\n"
            f"Lagerort: {item[6]}\n"
            f"Wert (€): {item[7]}\n"
            f"Bemerkungen: {item[8]}"
        )
        QMessageBox.information(self, "Produktinfo", info)

    def clear_inputs(self):
        self.name_input.clear()
        self.code_input.clear()
        self.location_input.clear()
        self.assigned_input.clear()
        self.subproject_input.clear()
        self.storage_input.clear()
        self.value_input.clear()
        self.remarks_input.clear()

    def refresh_list(self):
        self.products_list.clear()
        for p in database.get_all_products():
            self.products_list.addItem(f"{p[1]} — {p[2]} — {p[4]}")

    def export_csv(self):
        path = export_utils.export_to_csv()
        QMessageBox.information(self, "Exportiert", f"CSV-Datei gespeichert unter:\n{path}")
