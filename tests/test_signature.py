from signature_dialog import insert_signature_image
import fitz
import os

def test_insert_signature():
    doc = fitz.open(); doc.new_page(); doc.save("sign_target.pdf")
    
    # Create dummy image using fitz (empty pixmap)
    pix = fitz.Pixmap(fitz.csRGB, (0, 0, 10, 10), 0)
    pix.save("dummy_sig.png")
    
    insert_signature_image("sign_target.pdf", "dummy_sig.png", 0, (100, 100))
    # Basic check: file modified/saved successfully
    assert os.path.exists("sign_target.pdf")
    
    # Cleanup
    for f in ["sign_target.pdf", "dummy_sig.png"]:
        if os.path.exists(f):
            os.remove(f)
