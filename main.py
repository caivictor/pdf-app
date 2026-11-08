import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Application")
        self.resize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Toolbar
        toolbar_layout = QHBoxLayout()
        self.btn_open = QPushButton("[Open PDF]")
        self.btn_merge = QPushButton("[Merge PDFs]")
        self.btn_sign = QPushButton("[Sign PDF]")
        self.btn_print = QPushButton("[Print PDF]")
        toolbar_layout.addWidget(self.btn_open)
        toolbar_layout.addWidget(self.btn_merge)
        toolbar_layout.addWidget(self.btn_sign)
        toolbar_layout.addWidget(self.btn_print)
        main_layout.addLayout(toolbar_layout)

        # Canvas
        self.canvas = QLabel("No PDF Loaded")
        main_layout.addWidget(self.canvas)

        # Nav bar
        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton("[< Prev Page]")
        self.lbl_page = QLabel("Page 0 of 0")
        self.btn_next = QPushButton("[Next Page >]")
        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.lbl_page)
        nav_layout.addWidget(self.btn_next)
        main_layout.addLayout(nav_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
