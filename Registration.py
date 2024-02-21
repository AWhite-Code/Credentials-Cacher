from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt
import re
import pickle
from Hashing import Hashing

class RegistrationWidget(QWidget):
    def __init__(self, toggle_to_login):
        super().__init__()
        self.toggle_to_login = toggle_to_login
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        titleLabel = QLabel("Register")
        titleLabel.setAlignment(Qt.AlignCenter)

        # Using QGridLayout for input fields and labels
        gridLayout = QGridLayout()

        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Username...")
        
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Password...")
        self.password_entry.setEchoMode(QLineEdit.Password)
        
        self.confirm_password_entry = QLineEdit()
        self.confirm_password_entry.setPlaceholderText("Confirm Password...")
        self.confirm_password_entry.setEchoMode(QLineEdit.Password)
        
        password_requirements_label = QLabel("Password requirements:\n- Minimum 8 characters\n- At least one number\n- At least one special character")

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_action)

        self.switch_button = QPushButton("Switch to Login")
        self.switch_button.clicked.connect(self.toggle_to_login)

        gridLayout.addWidget(self.username_entry, 0, 0, 1, 2)
        gridLayout.addWidget(self.password_entry, 1, 0, 1, 2)
        gridLayout.addWidget(self.confirm_password_entry, 2, 0, 1, 2)
        gridLayout.addWidget(password_requirements_label, 3, 0, 1, 2)
        gridLayout.addWidget(self.register_button, 4, 0)
        gridLayout.addWidget(self.switch_button, 4, 1)

        layout.addWidget(titleLabel)
        layout.addLayout(gridLayout)
        self.setLayout(layout)

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