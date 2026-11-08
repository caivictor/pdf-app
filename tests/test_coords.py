from main import MainWindow
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QMouseEvent

def test_canvas_clicked_offset(qtbot, monkeypatch):
    window = MainWindow()
    
    captured_pos = None
    def mock_insert(path, img_path, page, pos):
        nonlocal captured_pos
        captured_pos = pos
        
    import main
    monkeypatch.setattr(main, "insert_signature_image", mock_insert)
    
    class FakeDoc:
        def close(self): pass
    window.viewer.doc = FakeDoc()
    window.viewer.file_path = "dummy.pdf"
    window.viewer.current_page = 0
    window.pending_signature_path = "sig.png"
    
    monkeypatch.setattr(window.viewer, "load_document", lambda *args: None)
    monkeypatch.setattr(window, "update_canvas", lambda *args: None)
    
    import PyQt6.QtWidgets
    def fake_info(*args): pass
    monkeypatch.setattr(PyQt6.QtWidgets.QMessageBox, "information", fake_info)
    
    # Just in case an error happens, we want to know
    def fake_crit(*args): print("ERROR:", args)
    monkeypatch.setattr(PyQt6.QtWidgets.QMessageBox, "critical", fake_crit)
    
    window.canvas.setGeometry(0, 0, 800, 600)
    class FakePixmap:
        def width(self): return 400
        def height(self): return 300
    monkeypatch.setattr(window.canvas, "pixmap", lambda: FakePixmap())
    
    event = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPointF(300, 200),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    window.canvas_clicked(event)
    
    assert captured_pos == (100, 50), f"Expected (100, 50), got {captured_pos}"
