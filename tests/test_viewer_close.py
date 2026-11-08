from pdf_viewer import PDFViewer
import fitz
import os

def test_viewer_close():
    doc = fitz.open(); doc.new_page(); doc.save("dummy_close.pdf")
    
    viewer = PDFViewer()
    viewer.load_document("dummy_close.pdf")
    assert viewer.doc is not None
    viewer.close_document()
    assert viewer.doc is None
    
    if os.path.exists("dummy_close.pdf"):
        os.remove("dummy_close.pdf")
