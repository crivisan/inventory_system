from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem,
    QCheckBox, QMessageBox, QHBoxLayout, QComboBox, QApplication
)
from PyQt6.QtCore import pyqtSignal, Qt, QTimer, QEventLoop
import database
import label_printer
import utils
import json
from pathlib import Path


class PrintWindow(QWidget):
    back_to_menu_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🖨️  Etiketten-Drucksystem – Land-lieben")
        self.setMinimumWidth(650)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>🖨️  Etiketten-Drucksystem</b>"))

        # --- top controls
        self.generate_btn = QPushButton("🔁 Codes generieren (falls fehlen)")
        self.print_all_btn = QPushButton("📦 Alle drucken")
        self.print_selected_btn = QPushButton("🖨️ Auswahl drucken")
        self.back_btn = QPushButton("⬅️ Zurück")

        row_top = QHBoxLayout()
        row_top.addWidget(self.generate_btn)
        row_top.addWidget(self.print_all_btn)
        layout.addLayout(row_top)

        # --- filters
        layout.addWidget(QLabel("Filter (optional):"))
        self.filter_gem = QComboBox()
        self.filter_proj = QComboBox()
        self.filter_gem.addItem("Alle Gemeinden")
        self.filter_proj.addItem("Alle Projekte")

        row_filter = QHBoxLayout()
        row_filter.addWidget(self.filter_gem)
        row_filter.addWidget(self.filter_proj)
        layout.addLayout(row_filter)

        # --- list of products
        layout.addWidget(QLabel("Produkte:"))
        self.listbox = QListWidget()
        layout.addWidget(self.listbox)

        layout.addWidget(self.print_selected_btn)
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

       # connections
        self.generate_btn.clicked.connect(self.generate_missing_codes)
        self.print_all_btn.clicked.connect(self.print_all)
        self.print_selected_btn.clicked.connect(self.print_selected)
        self.back_btn.clicked.connect(self.go_back)

        # show quick placeholder first
        self.listbox.addItem("⏳ Lädt Produkte ... bitte warten ...")

        # give the event loop a moment to draw the window, then load data
        QTimer.singleShot(200, self.populate_window)



    # --------------------------------------------------

    def load_filters(self):
        projs = set()
        gems = set()
        for p in database.get_all_products():
            if p[2]:
                gems.add(p[2])
            if p[17]:
                projs.add(p[17])
        for g in sorted(gems):
            self.filter_gem.addItem(g)
        for pr in sorted(projs):
            self.filter_proj.addItem(pr)

    # --------------------------------------------------

    def refresh_list(self):
        self.listbox.clear()
        gem_filter = self.filter_gem.currentText()
        proj_filter = self.filter_proj.currentText()
        for p in database.get_all_products():
            if gem_filter != "Alle Gemeinden" and p[2] != gem_filter:
                continue
            if proj_filter != "Alle Projekte" and p[17] != proj_filter:
                continue
            item = QListWidgetItem(f"{p[1]} — {p[2]} — {p[4]} — {p[7]}x")
            item.setData(1000, p)  # store product tuple
            item.setCheckState(Qt.CheckState.Unchecked)
            self.listbox.addItem(item)

    # --------------------------------------------------


    def generate_missing_codes(self):
        all_items = database.get_all_products()
        regenerated = 0
        for p in all_items:
            old_code = (p[1] or "").strip()
            abbr = (p[2] or "XXX")[:3].upper()
            new_code = utils.generate_code(abbr, p[0])

            if not old_code or not old_code.startswith(f"LL-{abbr.upper()}"):
                conn = database.get_connection()
                conn.execute("UPDATE products SET code=? WHERE id=?", (new_code, p[0]))
                conn.commit()
                conn.close()
                regenerated += 1

        QMessageBox.information(self, "Fertig", f"{regenerated} Codes neu generiert.")
        self.refresh_list()

    def generate_missing_codes2(self):
        """Regenerate codes for selected or all products."""
        from PyQt6.QtWidgets import QApplication
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        all_items = database.get_all_products()
        regenerated = 0
        for p in all_items:
            old_code = (p[1] or "").strip()
            abbr = (p[2] or "XXX")[:3].upper()
            new_code = utils.generate_code(abbr, p[0])

            # regenerate if empty OR doesn't follow new format
            if not old_code or "-" not in old_code or old_code != new_code:
                conn = database.get_connection()
                conn.execute("UPDATE products SET code=? WHERE id=?", (new_code, p[0]))
                conn.commit()
                conn.close()
                regenerated += 1

        QApplication.restoreOverrideCursor()
        QMessageBox.information(self, "Fertig", f"{regenerated} Codes neu generiert.")
        self.refresh_list()


    # --------------------------------------------------

    def selected_products(self):
        selected = []
        for i in range(self.listbox.count()):
            item = self.listbox.item(i)
            if item.checkState():
                selected.append(item.data(1000))
        return selected

    # --------------------------------------------------

    def print_selected(self):
        selected = []
        for i in range(self.listbox.count()):
            item = self.listbox.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected.append(item.data(1000))

        if not selected:
            QMessageBox.warning(self, "Hinweis", "Bitte mindestens ein Produkt auswählen.")
            return

        from label_printer import generate_labels
        files = generate_labels(selected)
        QMessageBox.information(self, "Erfolg", f"{len(files)} Etiketten generiert.")

    # --------------------------------------------------

    def print_all(self):
        from label_printer import generate_all_labels
        files = generate_all_labels()
        QMessageBox.information(self, "Fertig", f"{len(files)} Etiketten generiert.")


    # --------------------------------------------------

    def go_back(self):
        self.close()
        self.back_to_menu_requested.emit()

    def load_filters_and_list(self):
        """Load filters and list after UI is visible."""
        self.load_filters()
        self.refresh_list()


    def populate_window(self):
        QApplication.processEvents()  # let the UI render
        self.load_filters()
        self.refresh_list()
