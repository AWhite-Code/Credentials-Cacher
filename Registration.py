from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import re
import pickle
from Hashing import Hashing
from Database import Database
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

        # Logo setup
        dark_mode = self.main_window.settings.get('dark_mode', False)
        logo_path = "Icons/logo_white.png" if dark_mode else "Icons/logo.png"
        self.logo_label = QLabel(self)
        pixmap = QPixmap(logo_path)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.logo_label)

        # Form elements layout
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)

        # Adding labeled fields with spacers in between and setting them as attributes
        self.username_entry = self.add_labeled_field("Username:", "Enter your username", form_layout, field_name="username_entry")
        form_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        self.password_entry = self.add_labeled_field("Password:", "Enter your password", form_layout, True, field_name="password_entry")
        form_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        self.confirm_password_entry = self.add_labeled_field("Confirm Password:", "Confirm your password", form_layout, True, field_name="confirm_password_entry")
        form_layout.addItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Register button
        self.register_button = QPushButton("Register", self)
        form_layout.addWidget(self.register_button)
        self.register_button.clicked.connect(self.register_action)

        self.layout().addLayout(form_layout)

    def add_labeled_field(self, label_text, placeholder, layout, is_password=False, field_name=None):
        field_layout = QVBoxLayout()
        label = QLabel(label_text)
        field_layout.addWidget(label)
        
        field = QLineEdit(self)
        field.setPlaceholderText(placeholder)
        if is_password:
            field.setEchoMode(QLineEdit.Password)
        field_layout.addWidget(field)
        
        layout.addLayout(field_layout)
        
        if field_name:
            setattr(self, field_name, field)
            
        return field

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

    def show_credentials(self, username, hashed_password):
        credentials_info = f"Username: {username}\nHashed Password: {hashed_password}"
        QMessageBox.information(self, "Registration Details", credentials_info)

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
        # Dynamically adjust the logo and form fields based on the window size
        self.adjust_dynamic_components()

    def adjust_dynamic_components(self):
        # Adjust logo size based on window size
        logo_size = self.size() * 0.25  # or any other logic for sizing
        self.logo_label.setPixmap(self.logo_label.pixmap().scaled(int(logo_size.width()), int(logo_size.height()), Qt.KeepAspectRatio))

        # Adjust field widths based on window size
        field_width = self.size().width() * 0.4  # Adjust the factor as needed
        for field in self.findChildren(QLineEdit):
            field.setMaximumWidth(int(field_width))