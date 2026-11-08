import fitz
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt6.QtGui import QPainter, QPen, QImage, QPixmap
from PyQt6.QtCore import Qt, QPoint

def insert_signature_image(pdf_path, image_path, page_index, position):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_index)
    
    # Simple rectangle for signature
    x, y = position
    rect = fitz.Rect(x, y, x + 100, y + 50)
    page.insert_image(rect, filename=image_path)
    
    # Save inplace or to temp and replace
    tmp_path = pdf_path + ".tmp"
    doc.save(tmp_path)
    doc.close()
    
    import os
    os.replace(tmp_path, pdf_path)


class SignatureCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 200)
        self.image = QImage(self.size(), QImage.Format.Format_ARGB32)
        self.image.fill(Qt.GlobalColor.white)
        self.drawing = False
        self.last_point = QPoint()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()
            
    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.MouseButton.LeftButton) and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.GlobalColor.black, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()
            self.update()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False
            
    def clear(self):
        self.image.fill(Qt.GlobalColor.white)
        self.update()
        
class SignatureDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Draw Signature")
        self.selected_image_path = None
        
        layout = QVBoxLayout(self)
        
        self.canvas = SignatureCanvas()
        layout.addWidget(self.canvas)
        
        btn_layout = QHBoxLayout()
        self.btn_clear = QPushButton("[Clear]")
        self.btn_image = QPushButton("[Select Image]")
        self.btn_accept = QPushButton("[Accept]")
        
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_image)
        btn_layout.addWidget(self.btn_accept)
        layout.addLayout(btn_layout)
        
        self.btn_clear.clicked.connect(self.canvas.clear)
        self.btn_image.clicked.connect(self.select_image)
        self.btn_accept.clicked.connect(self.accept)
        
    def select_image(self):
        from PyQt6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getOpenFileName(self, "Select Signature Image", "", "Images (*.png *.jpg *.jpeg)")
        if filepath:
            self.selected_image_path = filepath
            self.accept()
        
    def get_signature_image_path(self):
        if self.selected_image_path:
            return self.selected_image_path
        tmp_path = "/tmp/signature_temp.png"
        self.canvas.image.save(tmp_path)
        return tmp_path