from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal

class ClickableLineEdit(QLineEdit):
    """
    A QLineEdit widget that toggles visibility (echo mode) between normal and password mode
    when clicked, unless a global setting enforces a specific visibility.

    Attributes:
        clicked (pyqtSignal): Signal emitted when the line edit is clicked.
    """
    clicked = pyqtSignal()  # Signal to indicate the field was clicked.

    def __init__(self, *args, **kwargs):
        """
        Initializes the ClickableLineEdit with optional arguments and keyword arguments
        for QLineEdit, and sets the default echo mode to password hiding.
        """
        super(ClickableLineEdit, self).__init__(*args, **kwargs)
        self.global_show_passwords = False  # Default to not showing passwords.
        self.setEchoMode(QLineEdit.Password)  # Set the default echo mode to hide the password.

    def mousePressEvent(self, event):
        """
        Handles mouse press events. Toggles the echo mode between showing and hiding the text,
        unless the global_show_passwords attribute enforces a specific state.

        Args:
            event: The event that triggered the mouse press.
        """
        # Only allow toggling if global settings do not enforce visibility.
        if not self.global_show_passwords:
            if self.echoMode() == QLineEdit.Password:
                self.setEchoMode(QLineEdit.Normal)
            else:
                self.setEchoMode(QLineEdit.Password)
        super(ClickableLineEdit, self).mousePressEvent(event)  # Ensure parent class's mouse press event is also handled.

    def applyGlobalVisibilitySetting(self, show_passwords):
        """
        Applies a global visibility setting, updating the echo mode accordingly.

        Args:
            show_passwords (bool): If True, passwords are shown; if False, they are hidden.
        """
        self.global_show_passwords = show_passwords
        self.setEchoMode(QLineEdit.Normal if show_passwords else QLineEdit.Password)

    def updateVisibility(self):
        """
        Updates the echo mode based on the current global_show_passwords setting.
        """
        if self.global_show_passwords:
            self.setEchoMode(QLineEdit.Normal)
        else:
            self.setEchoMode(QLineEdit.Password)
