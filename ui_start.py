from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QApplication
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from ui_main import InventoryApp
from ui_scan import ScanWindow

class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Land-lieben Inventar System")
        self.setFixedSize(400, 350)

        # --- Logo
        logo_label = QLabel()
        pixmap = QPixmap("./data/logo_landlieben.png")
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            logo_label.setText("Land-lieben")
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        # --- Buttons
        self.manage_btn = QPushButton("📦 Inventar verwalten")
        self.scan_btn = QPushButton("🔍 Lesemodus (Nur Scan)")

        for b in [self.manage_btn, self.scan_btn]:
            b.setMinimumHeight(45)
            b.setFont(QFont("Segoe UI", 11))

        # --- Layout
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(logo_label)
        layout.addStretch()
        layout.addWidget(self.manage_btn)
        layout.addWidget(self.scan_btn)
        layout.addStretch()
        self.setLayout(layout)

        # --- Signals
        self.manage_btn.clicked.connect(self.open_manage)
        self.scan_btn.clicked.connect(self.open_scan)

    def open_manage(self):
        self.inventory = InventoryApp(parent=self)
        self.inventory.show()
        self.hide()

    def open_scan(self):
        self.scan = ScanWindow(parent=self)
        self.scan.show()
        self.hide()
