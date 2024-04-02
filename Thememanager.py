from PyQt5.QtCore import QObject, pyqtSignal

class ThemeManager(QObject):
    themeChanged = pyqtSignal(str)  # Signal emitting the new theme name

    def __init__(self, application):
        super().__init__()
        self._application = application
        self._currentTheme = "light"  # Default theme
        self.applyCurrentTheme()

    def setTheme(self, themeName):
        if themeName != self._currentTheme:
            self._currentTheme = themeName
            self.applyCurrentTheme()
            self.themeChanged.emit(self._currentTheme)  # Emit signal on theme change

    def currentTheme(self):
        return self._currentTheme

    def applyCurrentTheme(self):
        themePath = f"{self._currentTheme}_theme.qss"
        try:
            with open(themePath, "r") as file:
                self._application.setStyleSheet(file.read())
        except FileNotFoundError:
            pass  # Handle missing theme file error
