from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
import database


class TableWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📋 Inventar Tabelle – Land-lieben")
        self.setMinimumSize(1200, 600)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        layout.addWidget(self.table)

        btn_row = QHBoxLayout()
        self.refresh_btn = QPushButton("🔄 Aktualisieren")
        self.save_btn = QPushButton("💾 Änderungen speichern")
        self.close_btn = QPushButton("⬅️ Zurück")
        btn_row.addWidget(self.refresh_btn)
        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.close_btn)
        layout.addLayout(btn_row)

        self.setLayout(layout)

        self.refresh_btn.clicked.connect(self.load_data)
        self.save_btn.clicked.connect(self.save_changes)
        self.close_btn.clicked.connect(self.close)

        self.load_data()

    # ------------------------------
    def load_data(self):
        products = database.get_all_products()
        headers = [
            "id", "code", "gemeinde", "einsatzort", "kategorie", "produkttyp",
            "produktdetails", "anzahl", "hersteller", "lieferant", "shop_link",
            "preis_netto", "preis_brutto", "bezahlt", "bestellt_am",
            "geliefert_am", "uebergeben_am", "projekt", "bemerkungen"
        ]
        self.table.clear()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(products))

        for row, prod in enumerate(products):
            for col, val in enumerate(prod):
                item = QTableWidgetItem(str(val) if val is not None else "")
                if col == 0:  # id column read-only
                    item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                self.table.setItem(row, col, item)
        self.table.resizeColumnsToContents()

    # ------------------------------
    def save_changes(self):
        conn = database.get_connection()
        cur = conn.cursor()
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        for row in range(rows):
            values = [self.table.item(row, c).text() if self.table.item(row, c) else None for c in range(cols)]
            # build SQL update dynamically
            cur.execute("""
                UPDATE products SET
                    code=?, gemeinde=?, einsatzort=?, kategorie=?, produkttyp=?, produktdetails=?, anzahl=?,
                    hersteller=?, lieferant=?, shop_link=?, preis_netto=?, preis_brutto=?, bezahlt=?,
                    bestellt_am=?, geliefert_am=?, uebergeben_am=?, projekt=?, bemerkungen=?
                WHERE id=?
            """, (
                values[1], values[2], values[3], values[4], values[5], values[6], values[7],
                values[8], values[9], values[10], values[11], values[12], values[13],
                values[14], values[15], values[16], values[17], values[18],
                values[0]
            ))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Gespeichert", "Alle Änderungen wurden gespeichert.")
