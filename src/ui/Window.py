from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget
from PyQt5.QtCore import QTimer
from .Login import LoginWidget
from .Vault_Window import VaultWidget
from .Registration import RegistrationWidget
import os
import pickle

class MainWindow(QMainWindow):
    def __init__(self, db, settings, themeManager):
        super().__init__()
        self.db = db  # Save the db instance for later use
        
        self.settings = settings  # Store settings
        self.themeManager = themeManager
        self.encryption_key = None  # New attribute for storing the encryption key
        
        self.autoLockTimer = QTimer(self)
        self.autoLockTimer.timeout.connect(self.logout)
        # Initialize the auto-lock timer based on settings, if auto-lock is enabled
        if settings.get("auto_lock_enabled", True):
            self.setAutoLockInterval(settings.get("auto_lock", 5))  # Default to 5 minutes if not set

        # Pass settings to VaultWidget
        self.vault_widget = VaultWidget(self.db, self.settings, self.themeManager, self, parent=self)
        
        self.setWindowTitle("Credentials Cacher")
        
        # Set initial size to 40% of the screen's width and height
        screen_size = QApplication.primaryScreen().size()
        width = int(screen_size.width() * 0.4)  # Ensure width is an integer
        height = int(screen_size.height() * 0.4)  # Ensure height is an integer
        self.resize(width, height)  # This should now work without type errors

        # Initialize stack for widgets
        self.stacked_widgets = QStackedWidget()
        self.setCentralWidget(self.stacked_widgets)

        # Initialize widgets
        self.login_widget = LoginWidget(self.toggle_widgets, self, self.db)
        self.registration_widget = RegistrationWidget(self.db, self)

        # Add widgets to the stack
        self.stacked_widgets.addWidget(self.registration_widget)
        self.stacked_widgets.addWidget(self.login_widget)
        self.stacked_widgets.addWidget(self.vault_widget)

        # Decide which widget to show on start
        self.current_widget = self.login_widget if self.check_credentials_exist() else self.registration_widget
        self.stacked_widgets.setCurrentWidget(self.current_widget)
        

    def toggle_widgets(self):
        if self.stacked_widgets.currentWidget() == self.login_widget:
            self.stacked_widgets.setCurrentWidget(self.registration_widget)
        else:
            self.stacked_widgets.setCurrentWidget(self.login_widget)

    def check_credentials_exist(self):
        app_data_path = os.getenv('APPDATA')  # Get the AppData path
        credentials_path = os.path.join(app_data_path, 'Credentials Cacher', 'credentials.bin')  # Path to the credentials file

        # Check if the credentials file exists and is not empty
        if os.path.exists(credentials_path):
            try:
                with open(credentials_path, 'rb') as file:  # Open the file from its new location
                    credentials = pickle.load(file)
                    return bool(credentials)  # Return True if credentials are not empty
            except EOFError:  # Handle empty file
                return False
        return False

    
    def set_encryption_key(self, key):
        self.encryption_key = key
        self.vault_widget.set_encryption_key(key)  # Pass the key to VaultWidget

    def clear_encryption_key(self):
        self.encryption_key = None
        self.vault_widget.set_encryption_key(None)  # Inform VaultWidget to clear the key

    def closeEvent(self, event):
        # First clear the encryption key without trying to repopulate the vault
        self.clear_encryption_key()  # This will now only clear the key and not try to repopulate the vault
        
        # Now it's safe to close the database connection
        self.db.close_connection()
        
        event.accept()  # Close the PYQT window normally
        
    def setAutoLockInterval(self, minutes):
        """Set the auto-lock timer interval and start the timer."""
        self.autoLockTimer.start(minutes * 60 * 1000)  # Convert minutes to milliseconds
        
    def resetAutoLockTimer(self):
        if self.settings.get("auto_lock_enabled", True):
            self.autoLockTimer.start(self.settings.get("auto_lock", 5) * 60 * 1000)

    def logout(self):
        """Handle logging out, clearing the encryption key, and switching to the login screen."""
        self.clear_encryption_key()  # Clear the encryption key
        self.stacked_widgets.setCurrentWidget(self.login_widget)  # Switch to login screen
        # Reset any necessary states or fields in the login screen
        self.login_widget.reset_state()
        
    def applyGlobalSettings(self):
        # Example: Apply theme settings
        newTheme = "dark" if self.settings['dark_mode'] else "light"
        self.themeManager.setTheme(newTheme)
        
        # Example: Reconfigure auto-lock timer
        if self.settings.get("auto_lock_enabled", True):
            self.setAutoLockInterval(self.settings.get("auto_lock", 5))
        else:
            self.autoLockTimer.stop()

            
    def show_login(self):
        self.stacked_widgets.setCurrentWidget(self.login_widget)
        self.login_widget.reset_state()
            
        
