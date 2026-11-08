import pytest
from main import MainWindow
from PyQt6.QtPrintSupport import QPrinterInfo
import PyQt6.QtWidgets

def test_print_no_printers(qtbot, monkeypatch):
    monkeypatch.setattr(QPrinterInfo, "availablePrinters", lambda: [])
    window = MainWindow()
    
    warned = False
    def mock_warning(*args):
        nonlocal warned
        warned = True
        
    monkeypatch.setattr(PyQt6.QtWidgets.QMessageBox, "warning", mock_warning)
    window.viewer.doc = type('obj', (object,), {'page_count': 1}) # fake doc
    
    # We also need to prevent QPrintDialog from blocking if it reaches there
    from PyQt6.QtPrintSupport import QPrintDialog
    def fake_exec(self):
        return PyQt6.QtWidgets.QDialog.DialogCode.Rejected
    monkeypatch.setattr(QPrintDialog, "exec", fake_exec)
    
    window.print_pdf()
    
    assert warned, "Should show warning when no printers are available"
