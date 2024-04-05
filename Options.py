from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QSlider, QLabel, QPushButton, QHBoxLayout
import json
from utils import get_settings_path
import os


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
        self.passwordVisibilityToggle = QCheckBox("Always Show Passwords")
        self.layout.addWidget(self.passwordVisibilityToggle)

        # Auto-Lock Toggle
        self.autoLockEnabledCheckbox = QCheckBox("Enable Auto-Lock")
        self.layout.addWidget(self.autoLockEnabledCheckbox)

        # Auto-Lock Timer
        self.autoLockLayout = QHBoxLayout()
        self.autoLockLabel = QLabel("Auto-lock timer (minutes): 5")  # Start at 5 minutes
        self.autoLockSlider = QSlider(Qt.Horizontal)
        self.autoLockSlider.setMinimum(1)  # 1 represents 5 minutes
        self.autoLockSlider.setMaximum(12)  # 12 represents 60 minutes (12 * 5 = 60)
        self.autoLockSlider.setTickInterval(1)  # Move in steps of 1
        self.autoLockSlider.setTickPosition(QSlider.TicksBelow)
        self.autoLockSlider.valueChanged.connect(lambda value: self.autoLockLabel.setText(f"Auto-lock timer (minutes): {value * 5}"))
        self.autoLockLayout.addWidget(self.autoLockLabel)
        self.autoLockLayout.addWidget(self.autoLockSlider)
        self.layout.addLayout(self.autoLockLayout)
        
        self.autoLockLayout.setContentsMargins(10, 0, 10, 0)  # Add left and right margins

        # OK and Cancel Buttons
        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.accept)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.reject)
        self.layout.addWidget(self.okButton)
        self.layout.addWidget(self.cancelButton)

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
                # Assuming the settings.json now also includes these:
                self.autoLockEnabledCheckbox.setChecked(settings.get('auto_lock_enabled', True))
        except FileNotFoundError:
            pass  # File doesn't exist, proceed with default values

        
    def load_or_create_settings():
        # Use the function to get the path to your settings file
        settings_path = get_settings_path()
        
        # Check if the settings file exists
        if not os.path.exists(settings_path):
            # If it doesn't exist, create a default settings object
            default_settings = {
                "darkMode": False,
                "passwordVisibility": False,
                "autoLockTimer": 300,  # Example: 300 seconds
                "remember_me": False,
                "passwordGenerator": {
                    "length": 12,
                    "includeUppercase": True,
                    "numDigits": 2,
                    "numSpecial": 2,
                    "includeNumbers": True,
                    "includeSpecial": True
                }
            }
            # Save the default settings to a new file
            with open(settings_path, 'w') as file:
                json.dump(default_settings, file, indent=4)
            # Return the default settings
            return default_settings
        
        # If the file exists, load the settings from the file
        with open(settings_path, 'r') as file:
            settings = json.load(file)
            return settings
        
    def accept(self):
        settings_path = get_settings_path()
        settings = {
            'dark_mode': self.darkModeToggle.isChecked(),
            'show_passwords': self.passwordVisibilityToggle.isChecked(),
            'auto_lock_enabled': self.autoLockEnabledCheckbox.isChecked(),
            'auto_lock': self.autoLockSlider.value() * 5,  # Convert slider value back to minutes
        }
        with open(settings_path, 'w') as file:
            json.dump(settings, file, indent=4)

        newTheme = "dark" if settings['dark_mode'] else "light"
        self.themeManager.setTheme(newTheme)
        self.parent().applyGlobalSettings() 

        super().accept()