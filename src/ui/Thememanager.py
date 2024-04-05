from PyQt5.QtCore import QObject, pyqtSignal
import json
import os
from core.utils import get_settings_path

class ThemeManager(QObject):
    themeChanged = pyqtSignal(str)  # Signal emitting the new theme name

    def __init__(self, application):
        super().__init__()
        self._application = application
        self._currentTheme = "light"  # Default to light theme
        self.loadAndApplyTheme()

    def loadAndApplyTheme(self):
        settings_path = get_settings_path()
        try:
            with open(settings_path, 'r') as file:
                settings = json.load(file)
                self.setTheme("dark" if settings.get('dark_mode', False) else "light")
        except FileNotFoundError:
            self.setTheme("light")  # Default to light theme if settings file is missing

    def setTheme(self, themeName):
        if themeName != self._currentTheme:
            self._currentTheme = themeName
            self.applyCurrentTheme()
            self.themeChanged.emit(self._currentTheme)

    def currentTheme(self):
        return self._currentTheme

    def applyCurrentTheme(self):
        # Adjust the path for the .qss file based on the current directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Go up three levels from this file
        themePath = os.path.join(base_dir, f"resources/styles/{self._currentTheme}_theme.qss")
        try:
            with open(themePath, "r") as file:
                self._application.setStyleSheet(file.read())
        except FileNotFoundError:
            pass  # Handle missing theme file error
