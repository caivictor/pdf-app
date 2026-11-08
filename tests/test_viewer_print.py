from pdf_viewer import PDFViewer
import fitz
import os

def test_viewer_print_render(qtbot):
    doc = fitz.open(); doc.new_page(); doc.save("dummy_print.pdf")
    
    viewer = PDFViewer()
    viewer.load_document("dummy_print.pdf")
    
    pix1 = viewer.render_page(0)
    pix2 = viewer.render_page_for_print(0)
    
    assert pix2.width() > pix1.width()
    
    viewer.close_document()
    if os.path.exists("dummy_print.pdf"):
        os.remove("dummy_print.pdf")
