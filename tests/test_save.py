import pytest
import fitz
from pdf_viewer import PDFViewer
import os

def test_save_pdf(tmp_path):
    # Setup initial PDF
    doc = fitz.open()
    doc.new_page()
    source_path = str(tmp_path / "source.pdf")
    doc.save(source_path)
    doc.close()

    # Load and save to new path
    viewer = PDFViewer()
    viewer.load_document(source_path)
    
    target_path = str(tmp_path / "target.pdf")
    viewer.save_document(target_path)
    
    # Verify save
    assert os.path.exists(target_path)
    saved_doc = fitz.open(target_path)
    assert saved_doc.page_count == 1
    saved_doc.close()
