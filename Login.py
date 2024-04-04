from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import pickle
from Hashing import Hashing
from Encryption import Encryption
import os

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

        # Assuming self.main_window.settings is a way to access settings
        # Replace this with your actual method of accessing settings
        dark_mode_enabled = self.main_window.settings.get('dark_mode', False)
        logo_path = "Icons/logo.png" if not dark_mode_enabled else "Icons/logo_white.png"

        # Logo
        logo_label = QLabel(self)
        pixmap = QPixmap(logo_path)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        # Grid layout to act as the 3x3 grid you described
        grid_layout = QHBoxLayout()
        grid_layout.setAlignment(Qt.AlignCenter)

        # Left spacer
        left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        grid_layout.addItem(left_spacer)

        # Central column for form elements
        central_column_layout = QVBoxLayout()
        central_column_layout.setAlignment(Qt.AlignCenter)

        # Username Entry
        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Username...")
        central_column_layout.addWidget(self.username_entry)

        # Password Entry
        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Password...")
        self.password_entry.setEchoMode(QLineEdit.Password)
        central_column_layout.addWidget(self.password_entry)

        # Remember Username Checkbox
        self.remember_check = QCheckBox("Remember Username", self)
        central_column_layout.addWidget(self.remember_check)

        # Spacer to add some distance between the "Remember Username" checkbox and the "Login" button
        medium_spacer = QWidget()
        medium_spacer.setFixedHeight(20)  # Adjust the height as needed for appropriate spacing
        central_column_layout.addWidget(medium_spacer)

        # Login Button
        self.login_button = QPushButton("Login", self)
        central_column_layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.login_action)

        # Spacer to add some distance between the login button and the forgot password label
        small_spacer = QWidget()
        small_spacer.setFixedHeight(10)  # Adjust the height as needed
        central_column_layout.addWidget(small_spacer)

        # Forgot my password Label
        self.forgot_password_label = QLabel("Forgot my password", self)
        self.forgot_password_label.setAlignment(Qt.AlignCenter)
        self.forgot_password_label.mousePressEvent = self.forgot_password
        central_column_layout.addWidget(self.forgot_password_label)

        # Add the central column to the grid layout
        grid_layout.addLayout(central_column_layout)

        # Right spacer
        right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        grid_layout.addItem(right_spacer)

        # Add the grid layout to the main layout
        main_layout.addLayout(grid_layout)

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
        self.remember_check.setChecked(False)