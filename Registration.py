from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
import re
import pickle
from Hashing import Hashing
import os

class RegistrationWidget(QWidget):
    def __init__(self, db, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        grid_layout = QHBoxLayout()
        left_column_layout = QVBoxLayout()
        left_column_layout.setAlignment(Qt.AlignTop)
        right_column_layout = QVBoxLayout()
        right_column_layout.setAlignment(Qt.AlignTop)

        # Left column setup (logo and password requirements)
        logo_layout = QHBoxLayout()
        logo_spacer = QWidget()
        logo_spacer.setFixedWidth(20)
        logo_layout.addWidget(logo_spacer)

        dark_mode_enabled = self.main_window.settings.get('dark_mode', False)
        logo_path = "Icons/logo.svg" if not dark_mode_enabled else "Icons/logo_white.svg"
        self.logoContainer = QSvgWidget(logo_path, self)
        logo_layout.addWidget(self.logoContainer)
        left_column_layout.addLayout(logo_layout)

        spacer = QWidget()
        spacer.setFixedHeight(20)
        left_column_layout.addWidget(spacer)

        password_requirements_text = self.create_password_requirements_label()
        left_column_layout.addWidget(password_requirements_text)

        # Right column setup (form fields and buttons)
        self.setup_form_fields(right_column_layout)

        credentials_path = os.path.join(os.getenv('APPDATA'), 'Credentials Cacher', 'credentials.bin')
        if os.path.exists(credentials_path):
            self.setup_return_to_login_button(right_column_layout)

        self.setup_register_button(right_column_layout)

        grid_layout.addLayout(left_column_layout, 2)
        grid_layout.addLayout(right_column_layout, 1)
        self.layout().addLayout(grid_layout)

    def create_password_requirements_label(self):
        # Function to create the password requirements label
        label_text = """<p><strong>Password Requirements:</strong></p>
                        <ul>
                            <li>20 Characters Long</li>
                            <li>Includes at least one number</li>
                            <li>Features one or more special character</li>
                            <li>Contains a mixture of upper and lower case characters</li>
                        </ul>"""
        label = QLabel(label_text, self)
        label.setTextFormat(Qt.RichText)
        return label

    def setup_form_fields(self, layout):
        # Function to setup form fields
        username_layout, self.username_entry = self.create_form_field("Username", "Enter your username")
        password_layout, self.password_entry = self.create_form_field("Password", "Enter your password", is_password=True)
        confirm_password_layout, self.confirm_password_entry = self.create_form_field("Confirm Password", "Confirm your password", is_password=True)

        layout.addLayout(username_layout)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addLayout(password_layout)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addLayout(confirm_password_layout)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def create_form_field(self, label_text, placeholder, is_password=False):
        # Function to create a form field with a label
        layout = QVBoxLayout()
        label = QLabel(label_text)
        field = QLineEdit(self)
        field.setPlaceholderText(placeholder)
        if is_password:
            field.setEchoMode(QLineEdit.Password)
        layout.addWidget(label)
        layout.addWidget(field)
        return layout, field

    def setup_return_to_login_button(self, layout):
        # Function to setup "Return to Login" button
        self.return_to_login_button = QPushButton("Return to Login", self)
        self.return_to_login_button.clicked.connect(self.main_window.show_login)
        layout.addWidget(self.return_to_login_button)

    def setup_register_button(self, layout):
        # Function to setup "Register" button
        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_action)
        layout.addWidget(self.register_button)


    def register_action(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        confirm_password = self.confirm_password_entry.text()

        if password != confirm_password:
            QMessageBox.warning(self, "Registration Failed", "Password and Confirm password do not match.")
        elif not self.validate_password(password):
            QMessageBox.warning(self, "Registration Failed", "Password does not meet requirements.")
        else:
            self.clear_credentials()
            hashed_password = Hashing.hash_password(password)
            self.save_credentials(username, hashed_password)
            QMessageBox.information(self, "Registration Success", "You have been registered successfully.")
            self.db.wipe_database()
            # Switch back to the login screen
            self.main_window.show_login()

    def clear_credentials(self):
        open('credentials.bin', 'wb').close()

    def validate_password(self, password):
        if len(password) < 8 or not re.search("[0-9]", password) or not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    def save_credentials(self, username, hashed_password):
        app_data_path = os.getenv('APPDATA')  # Get the AppData path
        app_directory = os.path.join(app_data_path, 'Credentials Cacher')  # Define your app's directory name

        if not os.path.exists(app_directory):
            os.makedirs(app_directory)  # Create the directory if it doesn't exist

        credentials_path = os.path.join(app_directory, 'credentials.bin')  # Path to the credentials file

        credentials = {'username': username, 'password': hashed_password}
        with open(credentials_path, 'wb') as file:
            pickle.dump(credentials, file)
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Dynamically adjust the logo size and margins
        logo_width = int(self.size().width() * 0.4)
        logo_height = int(self.size().height() * 0.55)
        self.logoContainer.setFixedSize(logo_width, logo_height)

        # Dynamically adjust the widths of QLineEdit widgets
        field_width = max(200, int(self.size().width() * 0.3))
        for field in [self.username_entry, self.password_entry, self.confirm_password_entry]:
            field.setMaximumWidth(field_width)