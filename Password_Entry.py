from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt

class PasswordEntryButton(QPushButton):
    """
    Custom QPushButton to represent a password entry in the vault.
    """
    def __init__(self, entry_data, display_function, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry_data = entry_data
        self.display_function = display_function
        self.initUI()

    def initUI(self):
        # Assuming the database entries are tuples in the order of the SQL table columns
        # e.g., (id, website_name, website_url, username, password, notes, created_at, updated_at)
        website_name = self.entry_data[1]  # Index 1 is website_name based on the SQL table structure
        self.setText(website_name)
        # Connect the button's clicked signal to the display function
        self.clicked.connect(lambda: self.display_function(self.entry_data))
        self.setCheckable(True)
        # Apply the custom style
        self.setStyle()
        self.setFocusPolicy(Qt.NoFocus)
        

    def setStyle(self):
        self.setStyleSheet("""
            QPushButton {
                border: 1px solid #a9a9a9;
                border-radius: 20px;
                padding: 10px;
                background-color: #f0f0f0;
                color: black;
                text-align: left;
                padding-left: 20px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed, QPushButton:checked {
                background-color: #F5C754;  /* Yellow color for the selected button */
            }
            QPushButton:focus {
                border: 1px solid #a9a9a9; /* Attempt to maintain the same border style on focus */
            }
        """)

    def display_details(self):
        # This method will be called when the button is clicked to display the entry details.
        # It will use the display function provided at initialization.
        self.display_function(self.entry_data)