from merge_dialog import merge_pdfs
import fitz
import os

def test_merge_two_pdfs():
    # Create two 1-page dummy PDFs
    doc1 = fitz.open(); doc1.new_page(); doc1.save("doc1.pdf")
    doc2 = fitz.open(); doc2.new_page(); doc2.save("doc2.pdf")
    
    merge_pdfs(["doc1.pdf", "doc2.pdf"], "merged.pdf")
    
    merged = fitz.open("merged.pdf")
    assert merged.page_count == 2
    
    # Cleanup
    for f in ["doc1.pdf", "doc2.pdf", "merged.pdf"]:
        if os.path.exists(f):
            os.remove(f)
