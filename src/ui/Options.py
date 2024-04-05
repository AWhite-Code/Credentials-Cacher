from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QSlider, QLabel, QPushButton, QHBoxLayout
import json
from core.utils import get_settings_path
import os

class OptionsDialog(QDialog):
    """
    Dialog for setting user preferences such as dark mode, password visibility, and auto-lock functionality.

    Attributes:
        themeManager (ThemeManager): A reference to the application's theme manager to apply theme changes.
    """
    def __init__(self, themeManager, parent=None):
        super().__init__(parent)
        self.themeManager = themeManager
        self.setWindowTitle("Options")
        self.layout = QVBoxLayout(self)

        # Setup UI components for various options.
        self.setupUIComponents()
        self.loadSettings()

    def setupUIComponents(self):
        """
        Initializes and adds UI components to the dialog.
        """
        # Dark Mode Toggle
        self.darkModeToggle = QCheckBox("Enable Dark Mode")
        self.layout.addWidget(self.darkModeToggle)

        # Password Visibility Toggle
        self.passwordVisibilityToggle = QCheckBox("Always Show Passwords")
        self.layout.addWidget(self.passwordVisibilityToggle)

        # Auto-Lock Feature Toggle
        self.autoLockEnabledCheckbox = QCheckBox("Enable Auto-Lock")
        self.layout.addWidget(self.autoLockEnabledCheckbox)

        # Auto-Lock Timer Slider and Label
        self.setupAutoLockTimer()

        # OK and Cancel Buttons
        self.setupDialogButtons()

    def setupAutoLockTimer(self):
        """
        Sets up the auto-lock timer slider and label.
        """
        self.autoLockLayout = QHBoxLayout()
        self.autoLockLabel = QLabel("Auto-lock timer (minutes): 5")  # Start at 5 minutes
        self.autoLockSlider = QSlider(Qt.Horizontal)
        self.autoLockSlider.setMinimum(1)  # Minimum represents 5 minutes
        self.autoLockSlider.setMaximum(12)  # Maximum represents 60 minutes
        self.autoLockSlider.setTickInterval(1)
        self.autoLockSlider.setTickPosition(QSlider.TicksBelow)
        self.autoLockSlider.valueChanged.connect(lambda value: self.autoLockLabel.setText(f"Auto-lock timer (minutes): {value * 5}"))
        self.autoLockLayout.addWidget(self.autoLockLabel)
        self.autoLockLayout.addWidget(self.autoLockSlider)
        self.layout.addLayout(self.autoLockLayout)
        
    def setupDialogButtons(self):
        """
        Sets up OK and Cancel buttons for the dialog.
        """
        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.accept)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.reject)
        self.layout.addWidget(self.okButton)
        self.layout.addWidget(self.cancelButton)

    def loadSettings(self):
        """
        Loads settings from a JSON file and applies them to the UI components.
        """
        settings_path = get_settings_path()
        try:
            with open(settings_path, 'r') as file:
                settings = json.load(file)
                self.darkModeToggle.setChecked(settings.get('dark_mode', False))
                self.passwordVisibilityToggle.setChecked(settings.get('show_passwords', False))
                self.autoLockEnabledCheckbox.setChecked(settings.get('auto_lock_enabled', True))
                self.autoLockSlider.setValue(settings.get('auto_lock', 1) // 5)
        except FileNotFoundError:
            pass  # Proceed with default values if the settings file does not exist

    @staticmethod
    def load_or_create_settings():
        """
        Loads settings from a file, creating a default settings file if it does not exist.

        Returns:
            dict: A dictionary of settings.
        """
        settings_path = get_settings_path()
        if not os.path.exists(settings_path):
            default_settings = { ... }  # Define default settings dictionary
            with open(settings_path, 'w') as file:
                json.dump(default_settings, file, indent=4)
            return default_settings
        else:
            with open(settings_path, 'r') as file:
                return json.load(file)

    def accept(self):
        """
        Overrides QDialog.accept to save settings and apply theme changes before closing the dialog.
        """
        settings_path = get_settings_path()
        settings = { ... }  # Gather settings from UI components
        with open(settings_path, 'w') as file:
            json.dump(settings, file, indent=4)
        self.themeManager.setTheme("dark" if settings['dark_mode'] else "light")
        self.parent().applyGlobalSettings() 
        super().accept()