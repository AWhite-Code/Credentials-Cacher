from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from Window import MainWindow
from Database import Database
from Thememanager import ThemeManager
from Options import OptionsDialog
import logging
import sys
import os

def get_settings_path():
    app_data_path = os.getenv('APPDATA')
    settings_directory = os.path.join(app_data_path, 'Credentials Cacher')
    if not os.path.exists(settings_directory):
        os.makedirs(settings_directory)
    return os.path.join(settings_directory, 'settings.json')

def main():
    db = Database()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)

    settings = OptionsDialog.load_or_create_settings()

    themeManager = ThemeManager(app)  # Initialize the theme manager with the QApplication instance
    themeManager.applyCurrentTheme()

    # Apply theme based on the darkMode setting from the JSON
    if settings.get("dark_mode", False):
        themeManager.setTheme("dark")
    else:
        themeManager.setTheme("light")

    main_window = MainWindow(db, settings, themeManager)
    main_window.show()
    app.exec_()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()