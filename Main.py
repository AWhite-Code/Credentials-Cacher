from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from Window import MainWindow
from Database import Database
import logging
import sys
import json
import os

# Default settings
default_settings = {
    'dark_mode': False,
    'show_passwords': True,
    'auto_lock': 10,  # Default to 10 minutes
    'clear_clipboard': True,
}

def initialize_settings(settings_file='settings.json', default_settings={}):
    """Check for the existence of the settings file and create it with default settings if not found."""
    if not os.path.exists(settings_file):
        with open(settings_file, 'w') as file:
            json.dump(default_settings, file)

def main():
    db = Database()

    # Enable high DPI scaling and use high DPI icons before QApplication instance is created
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # Use high DPI icons

    # Initialize default settings if the settings file does not exist
    initialize_settings(default_settings=default_settings)

    app = QApplication(sys.argv)  # Adjusted to pass sys.argv
    main_window = MainWindow(db)  # Pass settings to MainWindow if necessary
    main_window.show()  # Show the main window
    sys.exit(app.exec_())  # Adjusted for proper application exit

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()