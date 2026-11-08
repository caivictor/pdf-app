import pytest
from signature_dialog import SignatureDialog
from PyQt6.QtWidgets import QPushButton

def test_signature_dialog_has_image_button(qtbot):
    dialog = SignatureDialog()
    qtbot.addWidget(dialog)
    buttons = [btn.text() for btn in dialog.findChildren(QPushButton)]
    assert "[Select Image]" in buttons, "Missing [Select Image] button in SignatureDialog"
