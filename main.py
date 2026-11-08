import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from pdf_viewer import PDFViewer
from merge_dialog import MergeDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Application")
        self.resize(800, 600)
        self.viewer = PDFViewer()

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
        self.canvas.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        # Connections
        self.btn_open.clicked.connect(self.open_pdf)
        self.btn_merge.clicked.connect(self.open_merge_dialog)
        self.btn_prev.clicked.connect(self.prev_page)
        self.btn_next.clicked.connect(self.next_page)


    def open_merge_dialog(self):
        dialog = MergeDialog(self)
        dialog.exec()

    def open_pdf(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if filepath:
            try:
                self.viewer.load_document(filepath)
                self.update_canvas()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open PDF:\n{str(e)}")

    def update_canvas(self):
        if self.viewer.doc:
            pixmap = self.viewer.render_page(self.viewer.current_page)
            if pixmap:
                self.canvas.setPixmap(pixmap)
                self.lbl_page.setText(f"Page {self.viewer.current_page + 1} of {self.viewer.get_page_count()}")

    def prev_page(self):
        if self.viewer.doc and self.viewer.current_page > 0:
            self.viewer.current_page -= 1
            self.update_canvas()

    def next_page(self):
        if self.viewer.doc and self.viewer.current_page < self.viewer.get_page_count() - 1:
            self.viewer.current_page += 1
            self.update_canvas()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
