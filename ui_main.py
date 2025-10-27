from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QListWidget
)
import database
import barcode_utils

class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Inventory System")
        self.setMinimumWidth(400)

        # Widgets
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Product name")

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Product code (auto or manual)")

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")

        self.add_button = QPushButton("Add Product")
        self.scan_input = QLineEdit()
        self.scan_input.setPlaceholderText("Scan a barcode...")
        self.products_list = QListWidget()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Add new product:"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.code_input)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.add_button)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Scan product:"))
        layout.addWidget(self.scan_input)
        layout.addWidget(self.products_list)
        self.setLayout(layout)

        # Connections
        self.add_button.clicked.connect(self.add_product)
        self.scan_input.returnPressed.connect(self.scan_product)

        # Load existing
        self.refresh_list()

    def add_product(self):
        name = self.name_input.text().strip()
        code = self.code_input.text().strip() or f"CODE{len(database.get_all_products())+1:04}"
        quantity = int(self.quantity_input.text() or 0)

        if not name:
            QMessageBox.warning(self, "Error", "Product name required")
            return

        database.add_product(name, code, quantity)
        barcode_utils.generate_barcode(code)
        QMessageBox.information(self, "Success", f"Added '{name}' with code {code}")
        self.name_input.clear()
        self.code_input.clear()
        self.quantity_input.clear()
        self.refresh_list()

    def scan_product(self):
        code = self.scan_input.text().strip()
        product = database.get_product_by_code(code)
        if product:
            QMessageBox.information(self, "Found", f"Product: {product[1]}\nQty: {product[3]}")
        else:
            QMessageBox.warning(self, "Not found", "No product with that code.")
        self.scan_input.clear()

    def refresh_list(self):
        self.products_list.clear()
        for p in database.get_all_products():
            self.products_list.addItem(f"{p[1]} ({p[2]}) — Qty: {p[3]}")
