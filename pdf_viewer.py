import fitz
from PyQt6.QtGui import QImage, QPixmap

class PDFViewer:
    def __init__(self):
        self.doc = None
        self.current_page = 0
        self.file_path = None

    def load_document(self, filepath):
        self.file_path = filepath
        self.doc = fitz.open(filepath)
        self.current_page = 0

    def render_page(self, page_index):
        if not self.doc or page_index < 0 or page_index >= self.doc.page_count:
            return None
        page = self.doc.load_page(page_index)
        pix = page.get_pixmap()
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(img)

    def get_page_count(self):
        return self.doc.page_count if self.doc else 0

    def close_document(self):
        if self.doc:
            self.doc.close()
            self.doc = None

    def render_page_for_print(self, page_index, dpi=300):
        if not self.doc or page_index < 0 or page_index >= self.doc.page_count:
            return None
        page = self.doc.load_page(page_index)
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(img)
