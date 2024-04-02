from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from Window import MainWindow
from Database import Database
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
            "zoomLevel": 100,
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

    # Load or create settings at the start
    settings = load_or_create_settings()

# Pass settings to MainWindow
    main_window = MainWindow(db, settings)
    main_window.show()
    app.exec_()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()