from PyQt5.QtCore import QObject, pyqtSignal
import json
import os
from core.utils import get_settings_path

class ThemeManager(QObject):
    """
    Manages the theme of the application, allowing for dynamic changes between light and dark modes.

    Attributes:
        themeChanged (pyqtSignal): Signal emitted when the theme changes, carrying the new theme name as a string.
    """

    themeChanged = pyqtSignal(str)  # Signal emitting the new theme name

    def __init__(self, application):
        """
        Initializes the ThemeManager with the application context to apply stylesheets.

        Args:
            application: The main QApplication instance of the application.
        """
        super().__init__()
        self._application = application
        self._currentTheme = "light"  # Default to light theme
        self.loadAndApplyTheme()

    def loadAndApplyTheme(self):
        """
        Loads the theme setting from a settings file and applies the theme. Defaults to light theme if not specified.
        """
        settings_path = get_settings_path()
        try:
            with open(settings_path, 'r') as file:
                settings = json.load(file)
                self.setTheme("dark" if settings.get('dark_mode', False) else "light")
        except (FileNotFoundError, json.JSONDecodeError):
            # Default to light theme if settings file is missing or corrupted
            self.setTheme("light")

    def setTheme(self, themeName):
        """
        Sets the application theme and emits a signal if the theme has changed.

        Args:
            themeName (str): The name of the theme to apply. Should be 'light' or 'dark'.
        """
        if themeName != self._currentTheme:
            self._currentTheme = themeName
            self.applyCurrentTheme()
            self.themeChanged.emit(self._currentTheme)

    def currentTheme(self):
        """
        Retrieves the current theme name.

        Returns:
            str: The current theme name ('light' or 'dark').
        """
        return self._currentTheme

    def applyCurrentTheme(self):
        """
        Applies the current theme by loading the corresponding .qss file and setting it as the application's stylesheet.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Navigate up to the project root directory
        themePath = os.path.join(base_dir, f"resources/styles/{self._currentTheme}_theme.qss")
        try:
            with open(themePath, "r") as file:
                self._application.setStyleSheet(file.read())
        except FileNotFoundError:
            # If the theme file is missing, do not apply any stylesheet
            pass
