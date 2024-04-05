from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.Window import MainWindow
from core.Database import Database
from ui.Thememanager import ThemeManager
from ui.Options import OptionsDialog
import logging
import sys
import os

def get_settings_path():
    """
    Determines the file path for storing application settings.

    Returns:
        str: The file path where the settings JSON file is stored or will be created.
    """
    app_data_path = os.getenv('APPDATA')
    settings_directory = os.path.join(app_data_path, 'Credentials Cacher')
    if not os.path.exists(settings_directory):
        os.makedirs(settings_directory)
    return os.path.join(settings_directory, 'settings.json')

def main():
    """
    The main function to initialize and run the PyQt application.
    """
    db = Database()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # Enable scaling for high DPI displays.
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # Use high resolution icons.
    app = QApplication(sys.argv)

    settings = OptionsDialog.load_or_create_settings()  # Load application settings.

    themeManager = ThemeManager(app)  # Manage application themes.
    themeManager.applyCurrentTheme()  # Apply the current theme based on settings.

    main_window = MainWindow(db, settings, themeManager)  # Initialize the main window.
    main_window.show()  # Show the main window.
    app.exec_()  # Start the application's event loop.

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)  # Configure logging.
    main()  # Execute the main function.
