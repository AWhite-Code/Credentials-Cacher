from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal

class ClickableLineEdit(QLineEdit):
    # Signal to indicate the field was clicked. You might not need this if toggling is fully managed by global settings.
    clicked = pyqtSignal()  

class ClickableLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(ClickableLineEdit, self).__init__(*args, **kwargs)
        self.global_show_passwords = False  # Default to not showing passwords
        self.setEchoMode(QLineEdit.Password)

    def mousePressEvent(self, event):
        # Only allow toggling if global settings do not enforce visibility
        if not self.global_show_passwords:
            if self.echoMode() == QLineEdit.Password:
                self.setEchoMode(QLineEdit.Normal)
            else:
                self.setEchoMode(QLineEdit.Password)
        super(ClickableLineEdit, self).mousePressEvent(event)

    def applyGlobalVisibilitySetting(self, show_passwords):
        self.global_show_passwords = show_passwords
        self.setEchoMode(QLineEdit.Normal if show_passwords else QLineEdit.Password)

    def updateVisibility(self):
        """Update the echo mode based on the current setting."""
        if self.global_show_passwords:
            self.setEchoMode(QLineEdit.Normal)
        else:
            self.setEchoMode(QLineEdit.Password)