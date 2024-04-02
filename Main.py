from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from Window import MainWindow
from Database import Database
from Thememanager import ThemeManager  # Assuming you have a ThemeManager class defined
import logging
import sys
import os
import json

def get_settings_path():
    app_data_path = os.getenv('APPDATA')
    settings_directory = os.path.join(app_data_path, 'Credentials Cacher')
    if not os.path.exists(settings_directory):
        os.makedirs(settings_directory)
    return os.path.join(settings_directory, 'settings.json')

def load_or_create_settings():
    settings_path = get_settings_path()
    if not os.path.exists(settings_path):
        # If the settings file doesn't exist, create a default settings dictionary
        default_settings = {
            "darkMode": False,
            "passwordVisibility": False,
            "autoLockTimer": 300,  # Example default value in seconds
            "clipboardClearing": 30,  # Example default value in seconds
            "passwordGenerator": {
                "length": 12,
                "includeUppercase": True,
                "numDigits": 2,
                "numSpecial": 2,
                "includeNumbers": True,
                "includeSpecial": True
            }
        }
        # Save the default settings to the file
        with open(settings_path, 'w') as file:
            json.dump(default_settings, file, indent=4)
    # Load the settings
    with open(settings_path, 'r') as file:
        return json.load(file)


def main():
    db = Database()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)

    settings = load_or_create_settings()

    themeManager = ThemeManager(app)  # Initialize the theme manager with the QApplication instance

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