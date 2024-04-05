from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
import pickle
from core.Hashing import Hashing
from core.Encryption import Encryption
import os
import json

class LoginWidget(QWidget):
    """
    Widget for user login, including fields for username and password, a 'Remember Me' checkbox, 
    and a login button. Displays the logo and adapts to dark mode settings.
    
    Attributes:
        on_show_other_frame (Callable): Function to trigger the display of a different UI frame.
        main_window (MainWindow): The main application window instance for accessing global settings.
        db (Database): Database connection object, not used in this part but required for complete functionality.
    """

    def __init__(self, on_show_other_frame, main_window, db, parent=None):
        """
        Initializes the login widget with callback functions and main window reference.
        
        Args:
            on_show_other_frame (Callable): Function to switch to another part of the application UI.
            main_window (MainWindow): Reference to the main application window.
            db (Database): The application's database connection. Not directly used in this widget.
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.on_show_other_frame = on_show_other_frame
        self.main_window = main_window
        self.db = db
        self.init_ui()

    def init_ui(self):
        """
        Initializes UI components for the login interface, arranging them in a vertical layout.
        """
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        dark_mode_enabled = self.main_window.settings.get('dark_mode', False)
        logo_path = self.determine_logo_path(dark_mode_enabled)

        central_column_layout = QVBoxLayout()
        central_column_layout.setAlignment(Qt.AlignCenter)
        self.setup_logo(central_column_layout, logo_path)
        self.setup_form_fields(central_column_layout)
        self.setup_action_buttons(central_column_layout)

        main_layout.addLayout(central_column_layout)
        self.load_settings()

    def determine_logo_path(self, dark_mode_enabled):
        """
        Computes the file path for the logo, choosing between the standard and dark mode variants.
        
        Args:
            dark_mode_enabled (bool): Indicates whether dark mode is currently enabled.
        
        Returns:
            str: Path to the logo file suitable for the current mode.
        """
        base_dir = os.path.dirname(os.path.realpath(__file__))
        resources_dir = os.path.join(os.path.dirname(os.path.dirname(base_dir)), 'resources', 'icons')
        logo_filename = "logo_white.svg" if dark_mode_enabled else "logo.svg"
        return os.path.join(resources_dir, logo_filename)

    def setup_logo(self, layout, logo_path):
        """
        Configures and places the application logo within the given layout.
        
        Args:
            layout (QVBoxLayout): The layout to which the logo will be added.
            logo_path (str): The path to the logo file.
        """
        logo_widget = QSvgWidget(logo_path, self)
        layout.addWidget(logo_widget, alignment=Qt.AlignCenter)

    def setup_form_fields(self, layout):
        """
        Arranges username and password input fields within the specified layout.
        
        Args:
            layout (QVBoxLayout): The layout for placing the input fields.
        """
        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Username...")
        layout.addWidget(self.username_entry)

        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Password...")
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)

        self.remember_me_checkbox = QCheckBox("Remember Me", self)
        layout.addWidget(self.remember_me_checkbox)

    def setup_action_buttons(self, layout):
        """
        Adds login and forgot password buttons to the layout, with appropriate spacing.
        
        Args:
            layout (QVBoxLayout): The layout to contain the buttons.
        """
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login_action)
        layout.addWidget(self.login_button)

        forgot_password_label = QLabel("<a href='#'>Forgot my password</a>", self)
        forgot_password_label.setAlignment(Qt.AlignCenter)
        forgot_password_label.mousePressEvent = self.on_forgot_password_clicked
        layout.addWidget(forgot_password_label)

    def setup_forgot_password_label(self, layout):
        """
        Configures the "Forgot my password" label as a clickable link.

        Args:
            layout (QVBoxLayout): The layout where the label is to be added.
        """
        self.forgot_password_label = QLabel("Forgot my password", self)
        self.forgot_password_label.setAlignment(Qt.AlignCenter)
        self.forgot_password_label.setStyleSheet("color: blue; text-decoration: underline;")
        self.forgot_password_label.mousePressEvent = self.on_forgot_password_clicked
        layout.addWidget(self.forgot_password_label)

    def wrap_central_layout(self, main_layout, central_column_layout):
        """
        Centers the central column layout within the main layout by adding horizontal stretches.

        Args:
            main_layout (QVBoxLayout): The main layout of the widget.
            central_column_layout (QVBoxLayout): The layout containing form elements.
        """
        wrapper_layout = QHBoxLayout()
        wrapper_layout.addStretch()
        wrapper_layout.addLayout(central_column_layout)
        wrapper_layout.addStretch()
        main_layout.addLayout(wrapper_layout)

    def forgot_password(self, event):
        """
        Triggered when the "Forgot my password" label is clicked. Calls the function to switch views.

        Args:
            event: The mouse event.
        """
        self.on_show_other_frame()

    def login_action(self):
        """
        Validates the username and password against stored credentials. If successful, proceeds to the main application view.
        """
        username = self.username_entry.text().strip()
        password = self.password_entry.text().strip()

        if self.validate_login(username, password):
            global_salt = self.get_global_salt()
            encryption_key = Encryption.derive_key(password.encode(), global_salt)
            self.main_window.set_encryption_key(encryption_key)
            self.main_window.stacked_widgets.setCurrentWidget(self.main_window.vault_widget)
            self.save_settings()
        else:
            QMessageBox.warning(self, "Login Failed", "The username or password is incorrect.")

    def validate_login(self, username, password):
        """
        Checks the provided username and password against the stored credentials.

        Args:
            username (str): The entered username.
            password (str): The entered password.

        Returns:
            bool: True if the credentials match, False otherwise.
        """
        credentials_path = os.path.join(os.getenv('APPDATA'), 'Credentials Cacher', 'credentials.bin')

        try:
            with open(credentials_path, 'rb') as file:
                credentials = pickle.load(file)
                return Hashing.verify_password(credentials['password'], password) and credentials['username'] == username
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Credentials file not found.")
            return False
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            return False

    def get_global_salt(self):
        """
        Retrieves the global salt used for encryption from the stored file.

        Returns:
            bytes: The global salt, or None if the file could not be found.
        """
        salt_path = os.path.join(os.getenv('APPDATA'), 'Credentials Cacher', 'global_salt.bin')

        try:
            with open(salt_path, 'rb') as salt_file:
                return salt_file.read()
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Global salt file not found.")
            return None

    def reset_state(self):
        """
        Resets the input fields and checkboxes to their default state.
        """
        self.username_entry.clear()
        self.password_entry.clear()
        self.remember_me_checkbox.setChecked(False)

    def load_settings(self):
        """
        Loads user preferences from the settings file, applying any remembered username and the remember_me state.
        """
        settings_path = os.path.join(os.getenv('APPDATA'), 'Credentials Cacher', 'settings.json')

        try:
            with open(settings_path, 'r') as file:
                settings = json.load(file)
                
                # Check and apply the remember_me setting
                remember_me = settings.get('remember_me', False)
                self.remember_me_checkbox.setChecked(remember_me)
                
                if remember_me:
                    credentials_path = os.path.join(os.getenv('APPDATA'), 'Credentials Cacher', 'credentials.bin')
                    with open(credentials_path, 'rb') as cred_file:
                        credentials = pickle.load(cred_file)
                        self.username_entry.setText(credentials.get('username', ''))
                        # If you also want to autofill the password (not recommended for security reasons), you can do it here.
        except FileNotFoundError:
            # Settings file doesn't exist; proceed with defaults.
            pass
        except json.JSONDecodeError:
            print("Error reading settings file. It may be empty or corrupted.")

    def save_settings(self):
        """
        Saves the 'remember_me' preference to a JSON settings file.
        
        This method checks if the settings file exists, loads current settings if so, and updates 
        or adds the 'remember_me' preference based on the state of the associated checkbox in the UI.
        If the file doesn't exist, it creates a new settings dictionary and adds the 'remember_me' preference.
        The updated settings are then written back to the file.
        """
        # Construct the file path for the settings JSON in the user's AppData directory.
        settings_path = os.path.join(os.getenv('APPDATA'), 'Credentials Cacher', 'settings.json')
        try:
            # Load existing settings if available; otherwise, start with an empty dict.
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as file:
                    settings = json.load(file)
            else:
                settings = {}
            
            # Update 'remember_me' preference based on the checkbox state.
            settings['remember_me'] = self.remember_me_checkbox.isChecked()

            # Write the updated settings back to the settings file.
            with open(settings_path, 'w') as file:
                json.dump(settings, file, indent=4)
        except Exception as e:
            # Log any errors encountered during the process.
            print(f"Error saving settings: {e}")

    def resizeEvent(self, event):
        """
        Adjusts UI elements dynamically based on the widget's size changes.
        """
        if hasattr(self, 'logoContainer'):
            self.logoContainer.setFixedSize(int(self.size().width() * 0.3), int(self.size().height() * 0.4))
        for field in self.findChildren(QLineEdit):
            field.setMaximumWidth(max(200, int(self.size().width() * 0.5)))

    def on_forgot_password_clicked(self, event):
        """
        Handles clicks on the "Forgot my password" label, warning about vault wipe.
        """
        self.on_show_other_frame()
        QMessageBox.warning(self, "WARNING!", "Warning: Resetting your password will wipe your password vault clean as a security measure.")
