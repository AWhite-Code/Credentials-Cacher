from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QSlider, QLabel, QPushButton
import json
from PyQt5.QtCore import QSettings
from utils import get_settings_path


class OptionsDialog(QDialog):
    def __init__(self, themeManager, parent=None):
        super().__init__(parent)
        self.themeManager = themeManager
        self.setWindowTitle("Options")
        self.layout = QVBoxLayout(self)

        # Dark Mode Toggle
        self.darkModeToggle = QCheckBox("Enable Dark Mode")
        self.layout.addWidget(self.darkModeToggle)

        # Password Visibility
        self.passwordVisibilityToggle = QCheckBox("Show Passwords")
        self.layout.addWidget(self.passwordVisibilityToggle)

        # Auto-Lock Timer
        self.autoLockLabel = QLabel("Auto-lock timer (minutes):")
        self.autoLockSlider = QSlider(Qt.Horizontal)
        self.autoLockSlider.setMinimum(1)  # Minimum 1 minute
        self.autoLockSlider.setMaximum(60)  # Maximum 60 minutes
        self.autoLockSlider.setTickInterval(5)  # Tick every 5 minutes
        self.autoLockSlider.setTickPosition(QSlider.TicksBelow)
        self.autoLockValueLabel = QLabel("1")  # Default value
        self.autoLockSlider.valueChanged.connect(self.updateAutoLockLabel)
        self.layout.addWidget(self.autoLockLabel)
        self.layout.addWidget(self.autoLockSlider)
        self.layout.addWidget(self.autoLockValueLabel)

        # Clipboard Clearing
        self.clipboardClearingToggle = QCheckBox("Clear clipboard after copying password")
        self.layout.addWidget(self.clipboardClearingToggle)

        # OK and Cancel Buttons
        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.accept)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.reject)
        self.layout.addWidget(self.okButton)
        self.layout.addWidget(self.cancelButton)

        # Load settings
        self.loadSettings()
        
    def updateAutoLockLabel(self, value):
        self.autoLockValueLabel.setText(str(value))
        
    def loadSettings(self):
        settings_path = get_settings_path()
        try:
            with open(settings_path, 'r') as file:
                settings = json.load(file)
                self.darkModeToggle.setChecked(settings.get('dark_mode', False))
                self.passwordVisibilityToggle.setChecked(settings.get('show_passwords', False))
                self.autoLockSlider.setValue(settings.get('auto_lock', 1))
                self.clipboardClearingToggle.setChecked(settings.get('clear_clipboard', False))
        except FileNotFoundError:
            pass  # File doesn't exist, proceed with default values

    def accept(self):
        settings_path = get_settings_path()
        dark_mode_enabled = self.darkModeToggle.isChecked()

        # Save settings
        settings = {
            'dark_mode': dark_mode_enabled,
            'show_passwords': self.passwordVisibilityToggle.isChecked(),
            'auto_lock': self.autoLockSlider.value(),
            'clear_clipboard': self.clipboardClearingToggle.isChecked()
        }
        with open(settings_path, 'w') as file:
            json.dump(settings, file, indent=4)

        # Update the theme based on the dark mode setting
        newTheme = "dark" if dark_mode_enabled else "light"
        self.themeManager.setTheme(newTheme)

        super().accept()