from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import re
import pickle
from Hashing import Hashing

class RegistrationWidget(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        # Main layout to organize logo and form
        main_layout = QHBoxLayout()

        # Decide the logo based on the dark mode setting
        dark_mode = self.main_window.settings.get('dark_mode', False)
        logo_path = "Icons/logo_white.png" if dark_mode else "Icons/logo.png"
        self.logo_label = QLabel(self)
        pixmap = QPixmap(logo_path)
        self.logo_label.setPixmap(pixmap.scaled(320, 320, Qt.KeepAspectRatio))
        main_layout.addWidget(self.logo_label)

        # Form elements
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)

        # Use spacers to push the form down and to the right
        form_layout.addItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Adjust size for desired spacing

        # Adding labeled fields with spacers in between
        self.add_labeled_field("Username:", "Username...", form_layout)
        form_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))  # Small spacer after username entry

        self.add_labeled_field("Password:", "Password...", form_layout, True)
        form_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))  # Small spacer after password entry

        self.add_labeled_field("Re-enter Password:", "Confirm Password...", form_layout, True)
        form_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Larger spacer before register button

        # Register button
        self.register_button = QPushButton("Register", self)
        form_layout.addWidget(self.register_button)
        self.register_button.clicked.connect(self.register_action)

        # Wrap form layout in another layout to center it horizontally
        form_wrapper_layout = QHBoxLayout()
        form_wrapper_layout.addStretch(2)  # Increase stretch on the left to push everything more to the right
        form_wrapper_layout.addLayout(form_layout)
        form_wrapper_layout.addStretch(1)  # You can adjust this to manage the right-side spacing

        main_layout.addLayout(form_wrapper_layout)
        self.layout().addLayout(main_layout)

    def add_labeled_field(self, label_text, placeholder, layout, is_password=False):
        label = QLabel(label_text)
        layout.addWidget(label)

        field = QLineEdit(self)
        field.setPlaceholderText(placeholder)
        if is_password:
            field.setEchoMode(QLineEdit.Password)
        layout.addWidget(field)


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
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Dynamically adjust the logo size based on the window size
        width = self.size().width() * 0.25  # Calculate 25% of the parent width
        height = self.size().height() * 0.25  # Calculate 25% of the parent height
        self.logo_label.setPixmap(self.logo_label.pixmap().scaled(int(width), int(height), Qt.KeepAspectRatio))

        # Dynamically adjust form field widths
        for widget in self.findChildren(QLineEdit):
            widget.setMaximumWidth(int(self.size().width() / 3))