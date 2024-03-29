from PyQt5.QtWidgets import (
    QWidget, QPushButton, QFormLayout, QLineEdit, QGridLayout, QApplication
)

class VaultWidget(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()
        self.applyStylesheet()

    def init_ui(self):
        """Initializes the user interface."""
        gridLayout = QGridLayout(self)

        # Initialize "Add Password" button and configure its width.
        self.add_password_button = QPushButton("Add Password", self)
        self.adjustButtonWidth()
        # Place the "Add Password" button at the bottom-left corner.
        gridLayout.addWidget(self.add_password_button, 2, 0)

        # Initialize and configure the "Add Password" form.
        self.init_add_password_form()
        # Position the form in the center column, spanning multiple rows.
        gridLayout.addWidget(self.addPasswordFormWidget, 0, 1, 3, 2)

        # Connect the button click to toggle the form's visibility.
        self.add_password_button.clicked.connect(self.toggle_add_password_form)
        # Initially hide the form.
        self.addPasswordFormWidget.setVisible(False)

    def init_add_password_form(self):
        """Initializes the 'Add Password' form."""
        self.addPasswordFormWidget = QWidget()
        formLayout = QFormLayout(self.addPasswordFormWidget)

        # Initialize form fields.
        self.website_name_entry = QLineEdit()
        self.website_url_entry = QLineEdit()
        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.notes_entry = QLineEdit()
        self.submit_button = QPushButton("Submit")

        # Set password field to mask input.
        self.password_entry.setEchoMode(QLineEdit.Password)

        # Add form fields to the layout.
        formLayout.addRow("Website Name", self.website_name_entry)
        formLayout.addRow("Website URL", self.website_url_entry)
        formLayout.addRow("Username", self.username_entry)
        formLayout.addRow("Password", self.password_entry)
        formLayout.addRow("Notes", self.notes_entry)
        formLayout.addRow(self.submit_button)

        # Connect the submit button to the action method.
        self.submit_button.clicked.connect(self.submit_password_details)

    def toggle_add_password_form(self):
        """Toggles the visibility of the 'Add Password' form."""
        isVisible = self.addPasswordFormWidget.isVisible()
        self.addPasswordFormWidget.setVisible(not isVisible)

    def submit_password_details(self):
        """Handles the submission of password details."""
        # Collect data from form fields.
        website_name = self.website_name_entry.text()
        website_url = self.website_url_entry.text()
        username = self.username_entry.text()
        password = self.password_entry.text()
        notes = self.notes_entry.text()

        # Insert data into the database.
        self.db.add_password_entry(website_name, website_url, username, password, notes)

        # Clear form fields and hide the form.
        self.clear_form_fields()
        self.toggle_add_password_form()

    def clear_form_fields(self):
        """Clears all input fields in the form."""
        self.website_name_entry.clear()
        self.website_url_entry.clear()
        self.username_entry.clear()
        self.password_entry.clear()
        self.notes_entry.clear()

    def update_entries_list(self):
        """Updates the list of entries. Placeholder for implementation."""
        pass

    def init_password_details_display(self):
        """Initializes the display for password details. Placeholder for implementation."""
        pass

    def adjustButtonWidth(self):
        """Adjusts the width of the 'Add Password' button."""
        buttonWidth = int(self.width() * 0.2)
        self.add_password_button.setFixedWidth(buttonWidth)

    def applyStylesheet(self):
        """Applies the CSS stylesheet to the widget."""
        self.setStyleSheet("""
            QWidget {font: 15px;}
            QLineEdit {
                border: 2px solid #a9a9a9;
                border-radius: 15px;
                padding: 5px;
                background-color: white;
                color: black;
            }
            QLineEdit:hover {border: 2px solid #f0f0f0;}
            QPushButton {
                border: 2px solid #a9a9a9;
                border-radius: 15px;
                padding: 5px;
                background-color: #0078d7;
                color: white;
            }
            QPushButton:hover {background-color: #0053a6;}
            QPushButton:pressed {background-color: #00397a;}
        """)

    def resizeEvent(self, event):
        """Handles the widget's resize event."""
        self.adjustButtonWidth()
        super().resizeEvent(event)  # Call base class method to ensure proper event handling.
