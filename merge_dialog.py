import fitz
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QListWidget, QFileDialog, QMessageBox
)

def merge_pdfs(input_paths, output_path):
    merged = fitz.open()
    for path in input_paths:
        doc = fitz.open(path)
        merged.insert_pdf(doc)
    merged.save(output_path)

class MergeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Merge PDFs")
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("[Add File]")
        self.btn_up = QPushButton("[Move Up]")
        self.btn_down = QPushButton("[Move Down]")
        self.btn_combine = QPushButton("[Combine]")
        
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_up)
        btn_layout.addWidget(self.btn_down)
        btn_layout.addWidget(self.btn_combine)
        
        layout.addLayout(btn_layout)
        
        self.btn_add.clicked.connect(self.add_file)
        self.btn_up.clicked.connect(self.move_up)
        self.btn_down.clicked.connect(self.move_down)
        self.btn_combine.clicked.connect(self.combine)
        
    def add_file(self):
        filepaths, _ = QFileDialog.getOpenFileNames(self, "Add PDFs", "", "PDF Files (*.pdf)")
        for filepath in filepaths:
            self.list_widget.addItem(filepath)
            
    def move_up(self):
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row - 1, item)
            self.list_widget.setCurrentRow(current_row - 1)
            
    def move_down(self):
        current_row = self.list_widget.currentRow()
        if current_row >= 0 and current_row < self.list_widget.count() - 1:
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row + 1, item)
            self.list_widget.setCurrentRow(current_row + 1)
            
    def combine(self):
        if self.list_widget.count() < 2:
            QMessageBox.warning(self, "Warning", "Need at least 2 files to merge.")
            return
            
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "", "PDF Files (*.pdf)")
        if not output_path:
            return
            
        input_paths = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        try:
            merge_pdfs(input_paths, output_path)
            QMessageBox.information(self, "Success", "PDFs merged successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to merge:\n{str(e)}")
