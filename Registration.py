from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import re
import pickle
from Hashing import Hashing  # Ensure you have this module or similar functionality

class RegistrationWidget(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        # Main horizontal layout to split logo and form
        main_horizontal_layout = QHBoxLayout()

        # Logo setup with dark theme logic
        logo_label = QLabel(self)
        dark_mode = self.main_window.settings.get('dark_mode', False)
        logo_path = "Icons/logo_white.png" if dark_mode else "Icons/logo.png"
        pixmap = QPixmap(logo_path)
        logo_label.setPixmap(pixmap.scaled(320, 320, Qt.KeepAspectRatio))
        main_horizontal_layout.addWidget(logo_label)

        # Form elements setup
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)

        # Username with label above
        username_label = QLabel("Username:")
        form_layout.addWidget(username_label)
        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Username...")
        form_layout.addWidget(self.username_entry)

        form_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))  # Small spacer after username

        # Password with label above
        password_label = QLabel("Password:")
        form_layout.addWidget(password_label)
        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Password...")
        self.password_entry.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_entry)

        form_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))  # Small spacer after password

        # Confirm Password with label above
        confirm_password_label = QLabel("Re-enter Password:")
        form_layout.addWidget(confirm_password_label)
        self.confirm_password_entry = QLineEdit(self)
        self.confirm_password_entry.setPlaceholderText("Confirm Password...")
        self.confirm_password_entry.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.confirm_password_entry)

        form_layout.addItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Larger spacer before register button

        # Register button
        self.register_button = QPushButton("Register", self)
        form_layout.addWidget(self.register_button)
        self.register_button.clicked.connect(self.register_action)

        main_horizontal_layout.addLayout(form_layout)
        self.layout().addLayout(main_horizontal_layout)

    def register_action(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        confirm_password = self.confirm_password_entry.text()

        if password != confirm_password:
            QMessageBox.warning(self, "Registration Failed", "Password and Confirm password do not match")
        elif not self.validate_password(password):
            QMessageBox.warning(self, "Registration Failed", "Password does not meet requirements, please try again")
        else:
            self.clear_credentials()
            hashed_password = Hashing.hash_password(password)
            self.save_credentials(username, hashed_password)
            QMessageBox.information(self, "Registration Success", "You have been registered successfully.")
            self.show_credentials(username, hashed_password)
            self.toggle_to_login()

    def clear_credentials(self):
        open('credentials.bin', 'wb').close()

    def show_credentials(self, username, hashed_password):
        credentials_info = f"Username: {username}\nHashed Password: {hashed_password}"
        QMessageBox.information(self, "Registration Details", credentials_info)

    def validate_password(self, password):
        if len(password) < 8 or not re.search("[0-9]", password) or not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    def save_credentials(self, username, hashed_password):
        credentials = {'username': username, 'password': hashed_password}
        with open('credentials.bin', 'wb') as file:
            pickle.dump(credentials, file)