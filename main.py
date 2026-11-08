import sys
from PyQt6.QtWidgets import (
    QDialog,
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from pdf_viewer import PDFViewer
from merge_dialog import MergeDialog
from signature_dialog import SignatureDialog, insert_signature_image
from PyQt6.QtGui import QCursor, QPainter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

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
        self.btn_sign.clicked.connect(self.open_signature_dialog)
        self.btn_print.clicked.connect(self.print_pdf)

        self.pending_signature_path = None
        self.canvas.mousePressEvent = self.canvas_clicked
        self.btn_prev.clicked.connect(self.prev_page)
        self.btn_next.clicked.connect(self.next_page)



    def open_signature_dialog(self):
        if not self.viewer.doc:
            QMessageBox.warning(self, "Warning", "Please open a PDF first.")
            return
            
        dialog = SignatureDialog(self)
        if dialog.exec():
            self.pending_signature_path = dialog.get_signature_image_path()
            self.setCursor(QCursor(Qt.CursorShape.CrossCursor))
            


    def print_pdf(self):
        if not self.viewer.doc:
            QMessageBox.warning(self, "Warning", "Please open a PDF first.")
            return

        from PyQt6.QtPrintSupport import QPrinterInfo
        if not QPrinterInfo.availablePrinters():
            QMessageBox.warning(self, "Warning", "No system printers found.")
            return

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)

        dialog = QPrintDialog(printer, self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            painter = QPainter(printer)
            page_count = self.viewer.get_page_count()
            
            for i in range(page_count):
                if i > 0:
                    printer.newPage()
                
                # Render page
                pixmap = self.viewer.render_page_for_print(i, dpi=300)
                if pixmap:
                    image = pixmap.toImage()
                    
                    # Calculate scaling
                    rect = painter.viewport()
                    size = image.size()
                    size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
                    painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
                    painter.setWindow(image.rect())
                    
                    painter.drawImage(0, 0, image)
                    
            painter.end()
            QMessageBox.information(self, "Success", "Document sent to printer!")

    def canvas_clicked(self, event):
        if self.pending_signature_path and self.viewer.doc:
            # We need coordinates. Since QImage is scaled, we do a naive placement for now.
            x = event.position().x()
            y = event.position().y()
            
            # Adjust for center alignment
            pixmap = self.canvas.pixmap()
            if pixmap:
                offset_x = (self.canvas.width() - pixmap.width()) / 2.0
                offset_y = (self.canvas.height() - pixmap.height()) / 2.0
                x -= offset_x
                y -= offset_y
            
            try:
                self.viewer.close_document()
                insert_signature_image(self.viewer.file_path, self.pending_signature_path, self.viewer.current_page, (x, y))
                self.viewer.load_document(self.viewer.file_path)
                self.viewer.current_page = self.viewer.current_page # keep same page
                self.update_canvas()
                QMessageBox.information(self, "Success", "Signature added!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to sign:\n{str(e)}")
            finally:
                self.pending_signature_path = None
                self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

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
