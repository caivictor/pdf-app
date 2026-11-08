# Desktop PDF Application Design Specification

## 1. Overview and Purpose
A desktop application designed to view, visually sign, merge, and print PDF documents. The application is built with a focus on a clear, text-labeled user interface to ensure high compatibility with UI-TARS (an automated vision-based testing agent) configured to use Google Gemini API models.

## 2. Core Technologies
*   **Language:** Python 3
*   **UI Framework:** PyQt6 (Standard desktop widgets, chosen for accessibility and clear rendering).
*   **PDF Engine:** PyMuPDF (`fitz`) for rendering pages, modifying PDFs (inserting signatures), and merging documents.
*   **UI-TARS Testing:** The UI-TARS harness will be configured to utilize `google/gemini-1.5-pro` (or the latest Gemini equivalent) for its vision/reasoning model.

## 3. Architecture & User Interface Layout
The UI is designed for predictability and ease of parsing by vision-language models.
*   **Main Window:**
    *   **Top Toolbar:** High-contrast buttons with explicit text labels: `[Open PDF]`, `[Merge PDFs]`, `[Sign PDF]`, `[Print PDF]`.
    *   **Main Canvas:** Center screen `QLabel` displaying the current PDF page rendered as an image.
    *   **Bottom Bar:** Navigation controls: `[< Prev Page]`, `Page X of Y`, `[Next Page >]`.
*   **Modality:** All sub-tasks (Merging, Signing) will use modal dialogs to block the main window, preventing background interaction confusion for UI-TARS.

## 4. Feature Workflows

### 4.1 Viewing and Navigation
*   `PyMuPDF` converts the currently active page into a pixmap.
*   The pixmap is rendered into the main canvas `QLabel`.
*   Only the active page is held in memory as an image to optimize performance.

### 4.2 Merging PDFs
*   Clicking `[Merge PDFs]` opens a modal dialog.
*   **UI Elements:** A list view of selected files, `[Add File]`, `[Move Up]`, `[Move Down]`, and `[Combine]`.
*   **Action:** On `[Combine]`, PyMuPDF creates a new blank document, iterates over the file list, appends all pages from each, and prompts the user to save the new merged file.

### 4.3 Visual Signing (Wet Signature)
*   Clicking `[Sign PDF]` opens a modal dialog with two options:
    *   **Draw:** A blank canvas area to draw a signature using the mouse. Includes `[Clear]` and `[Accept]` buttons.
    *   **Image:** A button to select a local image file (PNG/JPG).
*   **Application:** Upon accepting, the cursor becomes a placement tool. Clicking on the main PDF canvas calculates the coordinates. PyMuPDF inserts the signature image at those exact coordinates on the active page and saves the document.

### 4.4 Printing
*   Clicking `[Print PDF]` passes the current PDF file path to the native OS print dialog via `PyQt6.QtPrintSupport`.

## 5. UI-TARS Testing Strategy
*   **Configuration:** UI-TARS will be explicitly configured in its environment/settings to route through the Google Gemini API.
*   **Design for Vision:** Avoid ambiguous iconography. All actionable elements must have descriptive text labels.
*   **Test Harness:** A `test_ui.py` script will be included to generate a dummy PDF and launch the app, allowing UI-TARS to autonomously verify the "Draw Signature" and "Merge" workflows end-to-end.
