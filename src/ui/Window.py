from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget
from PyQt5.QtCore import QTimer
from .Login import LoginWidget
from .Vault_Window import VaultWidget
from .Registration import RegistrationWidget
import os
import pickle

class MainWindow(QMainWindow):
    """
    The main window of the application, managing the transition between login, registration, and vault views.

    Attributes:
        db: Database connection to perform operations on the credentials database.
        settings: Application settings such as theme and auto-lock configurations.
        themeManager: Manages theme changes across the application.
        encryption_key: Key used for encrypting and decrypting the vault's content.
    """
    
    def __init__(self, db, settings, themeManager):
        """
        Initializes the MainWindow with necessary components like database, settings, and theme manager.

        Args:
            db: The database connection object.
            settings: A dictionary containing user preferences and settings.
            themeManager: An instance of ThemeManager for handling theme changes.
        """
        super().__init__()
        self.db = db
        self.settings = settings
        self.themeManager = themeManager
        self.encryption_key = None
        
        self.setupAutoLockTimer()
        self.initializeUI()
        
    def setupAutoLockTimer(self):
        """Initializes and configures the auto-lock timer based on user settings."""
        self.autoLockTimer = QTimer(self)
        self.autoLockTimer.timeout.connect(self.logout)
        if self.settings.get("auto_lock_enabled", True):
            self.setAutoLockInterval(self.settings.get("auto_lock", 5))
            
    def initializeUI(self):
        """Sets up UI components and stacks the widgets for different application states."""
        self.setWindowTitle("Credentials Cacher")
        self.resizeToFractionOfScreen()
        
        self.stacked_widgets = QStackedWidget()
        self.setCentralWidget(self.stacked_widgets)

        self.initWidgets()
        self.setCurrentWidgetBasedOnCredentials()

    def resizeToFractionOfScreen(self, fraction=0.4):
        """Resizes the main window to a fraction of the screen's size."""
        screen_size = QApplication.primaryScreen().size()
        self.resize(int(screen_size.width() * fraction), int(screen_size.height() * fraction))
    
    def initWidgets(self):
        """Initializes login, registration, and vault widgets and adds them to the stack."""
        self.login_widget = LoginWidget(self.toggle_widgets, self, self.db)
        self.registration_widget = RegistrationWidget(self.db, self)
        self.vault_widget = VaultWidget(self.db, self.settings, self.themeManager, self, parent=self)
        
        for widget in [self.registration_widget, self.login_widget, self.vault_widget]:
            self.stacked_widgets.addWidget(widget)
    
    def setCurrentWidgetBasedOnCredentials(self):
        """Determines and sets the initial widget to be displayed based on credentials existence."""
        self.current_widget = self.login_widget if self.check_credentials_exist() else self.registration_widget
        self.stacked_widgets.setCurrentWidget(self.current_widget)
    
    def toggle_widgets(self):
        """Toggles between the login and registration widgets."""
        next_widget = self.registration_widget if self.stacked_widgets.currentWidget() == self.login_widget else self.login_widget
        self.stacked_widgets.setCurrentWidget(next_widget)

    def check_credentials_exist(self):
        """Checks if the credentials file exists and contains data."""
        credentials_path = os.path.join(os.getenv('APPDATA'), 'Credentials Cacher', 'credentials.bin')
        return os.path.exists(credentials_path) and os.path.getsize(credentials_path) > 0

    
    def set_encryption_key(self, key):
        """
        Sets the encryption key for the session and updates the vault widget with the new key.

        Args:
            key: The encryption key to be used for encrypting and decrypting vault entries.
        """
        self.encryption_key = key
        self.vault_widget.set_encryption_key(key)

    def clear_encryption_key(self):
        """
        Clears the current encryption key from the session and notifies the vault widget to do the same.
        """
        self.encryption_key = None
        self.vault_widget.set_encryption_key(None)

    def closeEvent(self, event):
        """
        Handles the event triggered when the application window is closed. Ensures that the encryption key is cleared and the database connection is closed properly.

        Args:
            event: The close event.
        """
        self.clear_encryption_key()
        self.db.close_connection()
        event.accept()

    def setAutoLockInterval(self, minutes):
        """
        Sets the auto-lock timer interval based on the specified minutes and starts the timer.

        Args:
            minutes: The number of minutes after which the auto-lock should be triggered.
        """
        self.autoLockTimer.start(minutes * 60 * 1000)

    def resetAutoLockTimer(self):
        """
        Resets the auto-lock timer to the interval specified in the settings, if auto-lock is enabled.
        """
        if self.settings.get("auto_lock_enabled", True):
            self.setAutoLockInterval(self.settings.get("auto_lock", 5))

    def logout(self):
        """
        Logs out the current user by clearing the encryption key, switching to the login screen, and resetting the login form.
        """
        self.clear_encryption_key()
        self.stacked_widgets.setCurrentWidget(self.login_widget)
        self.login_widget.reset_state()

    def applyGlobalSettings(self):
        """
        Applies global settings such as theme changes and updates the auto-lock timer based on user preferences.
        """
        newTheme = "dark" if self.settings['dark_mode'] else "light"
        self.themeManager.setTheme(newTheme)
        if self.settings.get("auto_lock_enabled", True):
            self.setAutoLockInterval(self.settings.get("auto_lock", 5))
        else:
            self.autoLockTimer.stop()

    def show_login(self):
        """
        Switches the displayed widget to the login form and resets its state.
        """
        self.stacked_widgets.setCurrentWidget(self.login_widget)
        self.login_widget.reset_state()