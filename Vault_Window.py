from PyQt5.QtWidgets import (
    QWidget, QPushButton, QFormLayout, QLineEdit, QGridLayout, QApplication, QSpacerItem, QSizePolicy
)

class VaultWidget(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()
        self.applyStylesheet()

    def init_ui(self):
        gridLayout = QGridLayout(self)

        # "Add Password" button in the bottom-left corner (row 2, column 0)
        self.add_password_button = QPushButton("Add Password", self)
        gridLayout.addWidget(self.add_password_button, 2, 0)

        # Horizontal spacer to push the form to the right (already in place)
        spacerRight = QSpacerItem(20, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        gridLayout.addItem(spacerRight, 0, 0)

        # Initialize the "Add Password" form, set for the central column
        self.init_add_password_form()
        
        # Vertical spacer to push the form down
        spacerTop = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # Add the vertical spacer above the row where the form will be placed
        gridLayout.addItem(spacerTop, 0, 1)  # Adjust the position as needed

        # Now, place the form immediately below the vertical spacer
        gridLayout.addWidget(self.addPasswordFormWidget, 1, 1, 1, 1)  # Adjust grid placement as needed

        # Top-right corner spacer to maintain grid shape (if still necessary)
        gridLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 2)
        
        self.add_password_button.clicked.connect(self.toggle_add_password_form)
        self.addPasswordFormWidget.setVisible(False)

    def init_add_password_form(self):
        """Initializes the 'Add Password' form."""
        self.addPasswordFormWidget = QWidget()
        # Set the size policy for the form to be Preferred and Maximum, allowing it to shrink or expand as needed
        self.addPasswordFormWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        formLayout = QFormLayout(self.addPasswordFormWidget)
        formLayout.setVerticalSpacing(50)

        # Initialize form fields.
        self.website_name_entry = QLineEdit()
        self.website_url_entry = QLineEdit()
        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)  # Mask input for password
        self.notes_entry = QLineEdit()
        self.submit_button = QPushButton("Submit")

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
