from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
)

class VaultWidget(QWidget):
    def __init__(self, db, parent=None):
        super(VaultWidget, self).__init__(parent)
        self.db = db
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Title label at the top
        title_label = QLabel("Password Vault", self)
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Spacers to center the add password form
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Button layout for the Add Password button
        button_layout = QHBoxLayout()
        self.add_password_button = QPushButton("Add Password", self)
        button_layout.addWidget(self.add_password_button, alignment=Qt.AlignLeft)
        main_layout.addLayout(button_layout)

        # Add top spacer
        main_layout.addSpacerItem(top_spacer)

        # Form layout for the add password fields
        form_layout = QVBoxLayout()

        # Create the fields
        self.website_name_entry = QLineEdit(self)
        self.website_name_entry.setPlaceholderText("Website Name")
        self.website_url_entry = QLineEdit(self)
        self.website_url_entry.setPlaceholderText("Website URL")
        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Username")
        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Password")
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.notes_entry = QLineEdit(self)
        self.notes_entry.setPlaceholderText("Notes")

        # Add the fields to the form layout
        form_layout.addWidget(self.website_name_entry)
        form_layout.addWidget(self.website_url_entry)
        form_layout.addWidget(self.username_entry)
        form_layout.addWidget(self.password_entry)
        form_layout.addWidget(self.notes_entry)

        # Add the Submit button
        self.submit_button = QPushButton("Submit", self)
        form_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.submit_password_details)

        # Create a widget to hold the form layout
        self.form_widget = QWidget()
        self.form_widget.setLayout(form_layout)
        main_layout.addWidget(self.form_widget)

        # Add bottom spacer
        main_layout.addSpacerItem(bottom_spacer)

        # Initially hide the form widget
        self.form_widget.hide()

        # Connect the Add Password button
        self.add_password_button.clicked.connect(self.toggle_add_password_form)

        self.setLayout(main_layout)  # Set the layout on the widget

    def toggle_add_password_form(self):
        self.form_widget.setVisible(not self.form_widget.isVisible())

    def submit_password_details(self):
        # Collect data from the form fields
        website_name = self.website_name_entry.text()
        website_url = self.website_url_entry.text()
        username = self.username_entry.text()
        password = self.password_entry.text()
        notes = self.notes_entry.text()

        # Insert the data into the database
        self.db.add_password_entry(website_name, website_url, username, password, notes)

        # Clear the form fields
        self.website_name_entry.clear()
        self.website_url_entry.clear()
        self.username_entry.clear()
        self.password_entry.clear()
        self.notes_entry.clear()

        # Hide the form widget
        self.form_widget.hide()