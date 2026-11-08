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
    assert "[Save PDF]" in buttons
