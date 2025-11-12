from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from ui_main import InventoryApp
from ui_scan import ScanWindow
from ui_print import PrintWindow


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Land-lieben Inventar System")
        self.setFixedSize(420, 380)

        # --- Logo
        logo_label = QLabel()
        pixmap = QPixmap("logo_landlieben.png")
        if not pixmap.isNull():
            logo_label.setPixmap(
                pixmap.scaled(200, 200,
                              Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
            )
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            logo_label.setText("Land-lieben")
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        # --- Buttons
        self.manage_btn = QPushButton("📦 Inventar verwalten")
        self.scan_btn = QPushButton("🔍 Lesemodus (Nur Scan)")
        self.print_button = QPushButton("🖨️ Etiketten drucken")
        

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
        layout.addWidget(self.print_button)
        self.setLayout(layout)

        # --- Connections
        self.manage_btn.clicked.connect(self.open_manage)
        self.scan_btn.clicked.connect(self.open_scan)
        self.print_button.clicked.connect(self.open_print)

        # Keep refs
        self.inventory = None
        self.scan = None

    # ---------- open windows ----------
    def open_manage(self):
        self.inventory = InventoryApp()
        self.inventory.back_to_menu_requested.connect(self.show_again)
        self.inventory.show()
        self.hide()

    def open_scan(self):
        self.scan = ScanWindow()
        self.scan.back_to_menu_requested.connect(self.show_again)
        self.scan.show()
        self.hide()
    
    def open_print(self):
        self.print_window = PrintWindow()
        self.print_window.back_to_menu_requested.connect(self.show_again)
        self.print_window.show()
        self.hide()

    # ---------- return handler ----------
    def show_again(self):
        # when child emits signal, show menu again
        self.show()
