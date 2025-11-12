from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QListWidget, QComboBox, QDateEdit, QCheckBox,
    QScrollArea, QFrame, QListWidgetItem
)
from PyQt6.QtCore import QDate, pyqtSignal
import json
import database
import utils
import export_utils
import label_printer
from pathlib import Path
from ui_table import TableWindow



class InventoryApp(QWidget):
    back_to_menu_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Land-lieben Inventar System – Verwaltung")
        self.setMinimumWidth(650)


        # Load Gemeinde + VG data
        data_path = Path("./data/gemeinden.json")
        with open(data_path, "r", encoding="utf-8") as f:
            gdata = json.load(f)

        self.vg_box = QComboBox()
        self.vg_box.addItem("", "")
        for vg, abbr in gdata["VGs"].items():
            self.vg_box.addItem(f"{vg} (VG)", abbr)

        self.gem_box = QComboBox()
        self.gem_box.addItem("", "")
        for gem, abbr in gdata["Gemeinden"].items():
            self.gem_box.addItem(gem, abbr)

        # Identification fields
        self.einsatzort = QComboBox(); self.einsatzort.setEditable(True)
        self.kategorie = QComboBox(); self.kategorie.setEditable(True)
        self.produkttyp = QComboBox(); self.produkttyp.setEditable(True)
        self.produktdetails = QTextEdit()
        self.anzahl = QLineEdit("1")

        # Purchase info
        self.hersteller = QComboBox(); self.hersteller.setEditable(True)
        self.lieferant = QComboBox(); self.lieferant.setEditable(True)
        self.refresh_option_lists()
        self.shop_link = QLineEdit()
        self.preis_netto = QLineEdit()
        self.preis_brutto = QLineEdit()
        self.bezahlt = QCheckBox("Bezahlt")

        self.bestellt = QDateEdit(); self.bestellt.setCalendarPopup(True)
        self.geliefert = QDateEdit(); self.geliefert.setCalendarPopup(True)
        self.uebergeben = QDateEdit(); self.uebergeben.setCalendarPopup(True)
        for d in (self.bestellt, self.geliefert, self.uebergeben):
            d.setDate(QDate.currentDate())

        # Project / remarks
        self.projekt = QLineEdit()
        self.bemerkungen = QTextEdit()

        # Buttons
        self.add_btn = QPushButton("💾 Hinzufügen")
        self.table_btn = QPushButton("📋 Tabelle")
        self.export_btn = QPushButton("📤 Exportieren (CSV)")
        self.back_btn = QPushButton("⬅️ Zurück")

        self.listbox = QListWidget()

        # ---- Scrollable Content ----
        content = QWidget()
        inner_layout = QVBoxLayout(content)
        inner_layout.setContentsMargins(10, 10, 10, 10)
        inner_layout.setSpacing(8)

        # --- form content ---
        inner_layout.addWidget(QLabel("Gemeinde / VG"))
        inner_layout.addWidget(self.vg_box)
        inner_layout.addWidget(self.gem_box)
        inner_layout.addWidget(QLabel("Einsatzort"))
        inner_layout.addWidget(self.einsatzort)

        inner_layout.addWidget(QLabel("Kategorie / Produkttyp"))
        row = QHBoxLayout()
        row.addWidget(self.kategorie)
        row.addWidget(self.produkttyp)
        inner_layout.addLayout(row)

        inner_layout.addWidget(QLabel("Produktdetails"))
        inner_layout.addWidget(self.produktdetails)
        inner_layout.addWidget(QLabel("Anzahl"))
        inner_layout.addWidget(self.anzahl)

        inner_layout.addWidget(QLabel("Kauf- / Lieferinformationen"))
        inner_layout.addWidget(QLabel("Hersteller / Lieferant"))
        row2 = QHBoxLayout()
        row2.addWidget(self.hersteller)
        row2.addWidget(self.lieferant)
        inner_layout.addLayout(row2)

        inner_layout.addWidget(QLabel("Shop-Link"))
        inner_layout.addWidget(self.shop_link)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Preis netto"))
        row3.addWidget(self.preis_netto)
        row3.addWidget(QLabel("Preis brutto"))
        row3.addWidget(self.preis_brutto)
        inner_layout.addLayout(row3)

        inner_layout.addWidget(self.bezahlt)
        inner_layout.addWidget(QLabel("Bestellt / Geliefert / Übergeben"))
        rowd = QHBoxLayout()
        rowd.addWidget(self.bestellt)
        rowd.addWidget(self.geliefert)
        rowd.addWidget(self.uebergeben)
        inner_layout.addLayout(rowd)

        inner_layout.addWidget(QLabel("Projekt / Bemerkungen"))
        inner_layout.addWidget(self.projekt)
        inner_layout.addWidget(self.bemerkungen)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.table_btn)
        btn_row.addWidget(self.export_btn)
        btn_row.addWidget(self.back_btn)
        inner_layout.addLayout(btn_row)

        inner_layout.addWidget(QLabel("Bestehende Produkte"))
        inner_layout.addWidget(self.listbox)

        # ---- Wrap in ScrollArea ----
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.addWidget(scroll)
        self.setLayout(outer)

        # Connections
        self.add_btn.clicked.connect(self.add_product)
        self.table_btn.clicked.connect(self.open_table_window)
        self.export_btn.clicked.connect(self.export_csv)
        self.back_btn.clicked.connect(self.go_back)


        self.refresh_list()

    # ---- Actions ----
    def go_back(self):
        self.close()
        self.back_to_menu_requested.emit()

    def add_product(self):
        abbr = self.gem_box.currentData() or self.vg_box.currentData()
        gemeinde = self.gem_box.currentText() or self.vg_box.currentText()
        if not gemeinde or not abbr:
            QMessageBox.warning(self, "Fehler", "Bitte eine Gemeinde oder VG auswählen.")
            return

        purchase_date = self.bestellt.date().toString("yyyy-MM-dd")
        code = utils.generate_code(abbr, purchase_date)

        data = dict(
            code=code,
            gemeinde=gemeinde,
            einsatzort=self.einsatzort.currentText(),
            kategorie=self.kategorie.currentText(),
            produkttyp=self.produkttyp.currentText(),
            produktdetails=self.produktdetails.toPlainText(),
            anzahl=int(self.anzahl.text() or "1"),
            hersteller=self.hersteller.currentText(),
            lieferant=self.lieferant.currentText(),
            shop_link=self.shop_link.text(),
            preis_netto=float(self.preis_netto.text() or 0) if self.preis_netto.text() else None,
            preis_brutto=float(self.preis_brutto.text() or 0) if self.preis_brutto.text() else None,
            bezahlt="Ja" if self.bezahlt.isChecked() else "Nein",
            bestellt_am=self.bestellt.date().toString("yyyy-MM-dd"),
            geliefert_am=self.geliefert.date().toString("yyyy-MM-dd"),
            uebergeben_am=self.uebergeben.date().toString("yyyy-MM-dd"),
            projekt=self.projekt.text(),
            bemerkungen=self.bemerkungen.toPlainText()
        )

        try:
            # remember dropdown values for next time
            for field, combo in {
                "einsatzort": self.einsatzort,
                "kategorie": self.kategorie,
                "produkttyp": self.produkttyp,
                "hersteller": self.hersteller,
                "lieferant": self.lieferant
            }.items():
                database.add_option(field, combo.currentText())
            database.add_product_safe(**data)
            label_text = f"Land-lieben: {gemeinde} - {data['projekt']}"
            label_printer.make_pdf_label(code, label_text)
            QMessageBox.information(self, "Gespeichert", f"Produkt hinzugefügt\nCode: {code}")
            self.refresh_list()
        except Exception as e:
            QMessageBox.warning(self, "Fehler", str(e))

    def export_csv(self):
        path = export_utils.export_to_csv()
        QMessageBox.information(self, "Exportiert", f"CSV gespeichert unter:\n{path}")

    def refresh_list(self):
        self.listbox.clear()
        for p in database.get_all_products():
            item_text = f"{p[1]} – {p[2]} – {p[4]} – {p[5]}"
            list_item = QListWidgetItem(item_text)
            list_item.setData(1000, p)  # store the full product tuple
            self.listbox.addItem(list_item)


    def refresh_option_lists2(self):
        """Populate dropdowns from DB."""
        self.einsatzort.clear()
        self.kategorie.clear()
        self.produkttyp.clear()
        self.hersteller.clear()
        self.lieferant.clear()

        self.einsatzort.addItems(database.get_options("einsatzort"))
        self.kategorie.addItems(database.get_options("kategorie"))
        self.produkttyp.addItems(database.get_options("produkttyp"))
        self.hersteller.addItems(database.get_options("hersteller"))
        self.lieferant.addItems(database.get_options("lieferant"))

    def refresh_option_lists(self):
        """Populate dropdowns from DB with an empty first option."""
        for field, combo in {
            "einsatzort": self.einsatzort,
            "kategorie": self.kategorie,
            "produkttyp": self.produkttyp,
            "hersteller": self.hersteller,
            "lieferant": self.lieferant
        }.items():
            combo.clear()
            combo.addItem("")  # 👈 empty default option
            combo.addItems(database.get_options(field))
    
    def open_table_window(self):
        self.table_window = TableWindow()
        self.table_window.show()



