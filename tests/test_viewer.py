from pdf_viewer import PDFViewer
import fitz
import os

def test_load_and_render_page(qtbot):
    # Setup dummy PDF using fitz
    doc = fitz.open()
    doc.new_page()
    doc.save("dummy.pdf")
    
    viewer = PDFViewer()
    viewer.load_document("dummy.pdf")
    assert viewer.current_page == 0
    pixmap = viewer.render_page(0)
    assert pixmap is not None
    
    # Cleanup
    if os.path.exists("dummy.pdf"):
        os.remove("dummy.pdf")
