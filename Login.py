from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt
import pickle
from Hashing import Hashing
from Encryption import Encryption
import os

class LoginWidget(QWidget):
    def __init__(self, on_show_other_frame, main_window, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.on_show_other_frame = on_show_other_frame
        self.main_window = main_window 
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        # Create the title label
        title_label = QLabel("Credential Cacher", self)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label, 1, 0, 1, 3)

        # Create the username and password entries
        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Username...")
        layout.addWidget(self.username_entry, 3, 0, 1, 3)

        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Password...")
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry, 4, 0, 1, 3)

        # Create the forgot my password "hyperlink"
        self.forgot_password_label = QLabel("Forgot my password", self)
        self.forgot_password_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.forgot_password_label, 5, 1)
        self.forgot_password_label.mousePressEvent = self.forgot_password

        # Create a remember username checkbox
        self.remember_check = QCheckBox("Remember Username", self)
        layout.addWidget(self.remember_check, 6, 0, 1, 3)

        # Create the login button
        self.login_button = QPushButton("Login", self)
        layout.addWidget(self.login_button, 7, 0, 1, 3)
        self.login_button.clicked.connect(self.login_action)

    def forgot_password(self, event):
        self.on_show_other_frame()

    def login_action(self):
            username = self.username_entry.text()
            password = self.password_entry.text()

            if self.validate_login(username, password):
                # Derive the encryption key from the master password and global salt for the session
                global_salt = self.get_global_salt()
                encryption_key = Encryption.derive_key(password.encode(), global_salt)
                
                # Store the derived encryption key in the main window for use in cryptographic operations
                self.main_window.set_encryption_key(encryption_key)                
                self.main_window.stacked_widgets.setCurrentWidget(self.main_window.vault_widget)
            else:
                QMessageBox.warning(self, "Login Failed", "The username or password is incorrect.")


    def validate_login(self, username, password):
        try:
            with open('credentials.bin', 'rb') as file:
                credentials = pickle.load(file)
                if credentials['username'] == username:
                    return Hashing.verify_password(credentials['password'], password)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Credentials file not found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        return False

    def get_global_salt(self):
        # Load the global salt from a predefined location
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