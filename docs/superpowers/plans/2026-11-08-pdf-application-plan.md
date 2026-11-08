# PDF Application Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python/PyQt6 desktop application for viewing, visually signing, merging, and printing PDFs, optimized for UI-TARS automated testing.

**Architecture:** A monolithic PyQt6 desktop application using PyMuPDF for PDF rendering/manipulation, designed with accessible, text-labeled UI elements and modal dialogs for all sub-tasks to ensure reliable UI-TARS parsing.

**Tech Stack:** Python 3, PyQt6, PyMuPDF (fitz)

**Spec:** `docs/superpowers/specs/2026-11-08-pdf-application-design.md`

## Global Constraints

- **Language:** Python 3
- **Framework:** PyQt6
- **PDF Engine:** PyMuPDF (`fitz`)
- **UI:** High-contrast buttons, explicit text labels (no ambiguous icons), modal dialogs for sub-tasks.

## Review Focus

- Corrupted or invalid PDF files on open (should show error dialog, not crash).
- Merging PDFs with different page sizes (should preserve original page sizes).
- Drawing a signature outside the canvas bounds (should clip cleanly).
- Attempting to sign without a loaded PDF (button should be disabled or show error).
- Print failure due to no system printers (should gracefully notify user).

---

### Task 1: Project Scaffolding and Main Window UI

**Files:**
- Create: `main.py`
- Create: `pdf_viewer.py`
- Test: `tests/test_ui.py`

**Interfaces:**
- Consumes: None
- Produces: `MainWindow` class with labeled toolbar buttons (`[Open PDF]`, `[Merge PDFs]`, `[Sign PDF]`, `[Print PDF]`), central canvas (`QLabel`), and bottom navigation bar.

- [ ] **Step 1: Write the basic UI test**

```python
# tests/test_ui.py
import sys
from PyQt6.QtWidgets import QApplication, QPushButton
from main import MainWindow

def test_main_window_loads(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "PDF Application"
    # Check for presence of required buttons by text
    buttons = [btn.text() for btn in window.findChildren(QPushButton)]
    assert "[Open PDF]" in buttons
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_ui.py -v`
Expected: FAIL (main module not found)

- [ ] **Step 3: Implement `MainWindow` in `main.py`**

Set up the basic PyQt6 window layout according to the spec (Toolbar, Canvas, Nav bar). Use explicit text labels. Do not wire up PDF logic yet.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_ui.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add main.py tests/test_ui.py
git commit -m "feat: scaffold main window UI"
```

### Task 2: PDF Viewing and Navigation

**Files:**
- Modify: `main.py`
- Modify: `pdf_viewer.py`
- Test: `tests/test_viewer.py`

**Interfaces:**
- Consumes: `MainWindow` UI from Task 1.
- Produces: `PDFViewer` logic to load a PyMuPDF document, render a specific page to a QPixmap, and update the UI.

- [ ] **Step 1: Write the viewer logic test**

```python
# tests/test_viewer.py
from pdf_viewer import PDFViewer
import fitz

def test_load_and_render_page():
    # Setup dummy PDF using fitz
    doc = fitz.open()
    doc.new_page()
    doc.save("dummy.pdf")
    
    viewer = PDFViewer()
    viewer.load_document("dummy.pdf")
    assert viewer.current_page == 0
    pixmap = viewer.render_page(0)
    assert pixmap is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_viewer.py -v`
Expected: FAIL

- [ ] **Step 3: Implement PDF loading and rendering in `pdf_viewer.py`**

Use `fitz.open()` to load. Use `page.get_pixmap()` and convert to `QImage` then `QPixmap` for the UI. Wire up the `[Open PDF]` button (file dialog) and Next/Prev buttons in `main.py`.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_viewer.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add main.py pdf_viewer.py tests/test_viewer.py
git commit -m "feat: implement PDF viewing and navigation"
```

### Task 3: PDF Merging

**Files:**
- Create: `merge_dialog.py`
- Modify: `main.py`
- Test: `tests/test_merge.py`

**Interfaces:**
- Consumes: `fitz` for PDF operations.
- Produces: `MergeDialog` modal UI and PDF merging logic.

- [ ] **Step 1: Write the merge logic test**

```python
# tests/test_merge.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_merge.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `MergeDialog` and `merge_pdfs`**

Create the modal dialog with Add, Move Up/Down, Combine buttons. Implement `merge_pdfs` using PyMuPDF (`fitz.open()` new doc, `insert_pdf()` for each source). Wire `[Merge PDFs]` button in `main.py`.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_merge.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add main.py merge_dialog.py tests/test_merge.py
git commit -m "feat: implement PDF merging"
```

### Task 4: Visual Signing (Drawing Canvas)

**Files:**
- Create: `signature_dialog.py`
- Modify: `main.py`
- Test: `tests/test_signature.py`

**Interfaces:**
- Consumes: `fitz` for image insertion.
- Produces: `SignatureDialog` modal UI (drawing canvas) and logic to save signature as image and stamp it onto the PDF.

- [ ] **Step 1: Write the signature insertion test**

```python
# tests/test_signature.py
from signature_dialog import insert_signature_image
import fitz
import os

def test_insert_signature():
    doc = fitz.open(); doc.new_page(); doc.save("sign_target.pdf")
    # Create dummy image
    # ...
    insert_signature_image("sign_target.pdf", "dummy_sig.png", 0, (100, 100))
    # Basic check: file modified/saved successfully
    assert os.path.exists("sign_target.pdf")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_signature.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `SignatureDialog`**

Create a modal dialog with a drawing area (subclass QWidget, override `mouseMoveEvent`, `paintEvent`). Add `[Clear]` and `[Accept]` buttons. On accept, save the drawing to a temporary PNG. 
Modify `main.py` to change cursor state upon acceptance, capture the next click on the main canvas to get coordinates, and use PyMuPDF (`page.insert_image()`) to stamp the temporary PNG onto the PDF.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_signature.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add main.py signature_dialog.py tests/test_signature.py
git commit -m "feat: implement visual signature drawing and stamping"
```

### Task 5: Printing and Tying it Together

**Files:**
- Modify: `main.py`

**Interfaces:**
- Consumes: `QPrinter`, `QPrintDialog`

- [ ] **Step 1: Implement Printing**

Wire the `[Print PDF]` button. Since PyMuPDF doesn't print directly via PyQt easily, the simplest approach for a UI-centric app on Linux is often to spawn a print process or use QPrinter if we render all pages to images (which is memory intensive). Given the spec asks for native printing via `QtPrintSupport`, implement a print loop that renders pages to QImage and draws them onto a `QPrinter` via `QPainter`.

- [ ] **Step 2: Commit**

```bash
git add main.py
git commit -m "feat: implement PDF printing support"
```
