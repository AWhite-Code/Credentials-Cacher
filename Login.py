from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel, QLineEdit, QPushButton, QCheckBox, QFrame, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
import pickle
from Hashing import Hashing
from Encryption import Encryption
from ClickableLineEdit import ClickableLineEdit
import os
import json

class LoginWidget(QWidget):
    def __init__(self, on_show_other_frame, main_window, db, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.on_show_other_frame = on_show_other_frame
        self.main_window = main_window
        self.db = db
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        dark_mode_enabled = self.main_window.settings.get('dark_mode', False)
        logo_path = "Icons/logo.svg" if not dark_mode_enabled else "Icons/logo_white.svg"

        central_column_layout = QVBoxLayout()
        central_column_layout.setAlignment(Qt.AlignCenter)

        # Create a new QHBoxLayout for the logo and its spacer
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)

        # Spacer to push the logo to the right
        left_spacer_for_logo = QSpacerItem(5, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        logo_layout.addItem(left_spacer_for_logo)  # Add the spacer to the layout

        # Using QSvgWidget for SVG logo handling
        self.logoContainer = QSvgWidget(logo_path, self)
        logo_layout.addWidget(self.logoContainer)  # Add the logo to the layout

        central_column_layout.addLayout(logo_layout)  # Add the logo layout to the central column

        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Username...")
        central_column_layout.addWidget(self.username_entry)

        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Password...")
        self.password_entry.setEchoMode(QLineEdit.Password)
        central_column_layout.addWidget(self.password_entry)

        self.remember_me_checkbox = QCheckBox("Remember Me", self)
        central_column_layout.addWidget(self.remember_me_checkbox)

        medium_spacer = QWidget()
        medium_spacer.setFixedHeight(20)
        central_column_layout.addWidget(medium_spacer)

        self.login_button = QPushButton("Login", self)
        central_column_layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.login_action)

        small_spacer = QWidget()
        small_spacer.setFixedHeight(10)
        central_column_layout.addWidget(small_spacer)

        self.forgot_password_label = QLabel("Forgot my password", self)
        self.forgot_password_label.setAlignment(Qt.AlignCenter)
        # Make the text appear like a link
        self.forgot_password_label.setStyleSheet("QLabel { color : blue; text-decoration: underline; }")
        # Add to layout
        central_column_layout.addWidget(self.forgot_password_label)
        # Connect the mouse press event
        self.forgot_password_label.mousePressEvent = self.on_forgot_password_clicked

        # Wrapping central_column_layout in another QHBoxLayout to center it
        wrapper_layout = QHBoxLayout()
        wrapper_layout.addStretch()  # This adds a flexible space before central_column_layout that expands
        wrapper_layout.addLayout(central_column_layout)  # Add central_column_layout which we want to center
        wrapper_layout.addStretch()  # This adds a flexible space after central_column_layout that expands

        main_layout.addLayout(wrapper_layout)

        self.load_settings()
        
    def forgot_password(self, event):
        self.on_show_other_frame()

    def login_action(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        if self.validate_login(username, password):
            global_salt = self.get_global_salt()
            encryption_key = Encryption.derive_key(password.encode(), global_salt)
            self.main_window.set_encryption_key(encryption_key)
            self.main_window.stacked_widgets.setCurrentWidget(self.main_window.vault_widget)
            self.save_settings()
        else:
            QMessageBox.warning(self, "Login Failed", "The username or password is incorrect.")

    def validate_login(self, username, password):
        app_data_path = os.getenv('APPDATA')  # Get the AppData path
        credentials_path = os.path.join(app_data_path, 'Credentials Cacher', 'credentials.bin')  # Path to the credentials file

        try:
            with open(credentials_path, 'rb') as file:
                credentials = pickle.load(file)
                if credentials['username'] == username:
                    return Hashing.verify_password(credentials['password'], password)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Credentials file not found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        return False

    def get_global_salt(self):
        salt_path = os.path.join(os.getenv('APPDATA'), 'Credentials Cacher', 'global_salt.bin')
        try:
            with open(salt_path, 'rb') as salt_file:
                return salt_file.read()
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Global salt file not found.")
            return None

    def reset_state(self):
        """Reset the login form to its default state."""
        self.username_entry.clear()
        self.password_entry.clear()
        self.remember_me_checkbox.setChecked(False)
        

    def load_settings(self):
        settings_path = os.path.join(os.getenv('APPDATA'), 'Credentials Cacher', 'settings.json')
        try:
            with open(settings_path, 'r') as file:
                settings = json.load(file)
                if settings.get('remember_me', False):
                    self.remember_me_checkbox.setChecked(True)
                    # Load username from credentials.bin
                    credentials_path = os.path.join(os.getenv('APPDATA'), 'Credentials Cacher', 'credentials.bin')
                    with open(credentials_path, 'rb') as cred_file:
                        credentials = pickle.load(cred_file)
                        self.username_entry.setText(credentials['username'])
        except FileNotFoundError:
            pass

            
    def save_settings(self):
        # Method to save 'remember_me' setting without storing username
        settings_path = os.path.join(os.getenv('APPDATA'), 'Credentials Cacher', 'settings.json')
        try:
            with open(settings_path, 'r') as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = {}

        settings['remember_me'] = self.remember_me_checkbox.isChecked()

        with open(settings_path, 'w') as file:
            json.dump(settings, file, indent=4)
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Ensure the dimensions are integers
        logo_width = int(self.size().width() * 0.3)
        logo_height = int(self.size().height() * 0.4)
        self.logoContainer.setFixedSize(logo_width, logo_height)

        # Adjust the widths of QLineEdit widgets
        field_width = max(200, int(self.size().width() * 0.5))
        for field in self.findChildren(QLineEdit):
            field.setMaximumWidth(field_width)
            
    def on_forgot_password_clicked(self, event):
        # Call the function to switch view to RegistrationWidget
        self.on_show_other_frame()
