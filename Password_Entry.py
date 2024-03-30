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
        website_name = self.entry_data[1]  # Index 1 is website_name based on the SQL table structure
        self.setText(website_name)
        self.clicked.connect(lambda: self.display_details())
        self.setCheckable(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.updateStyle(False)  # Initialize with the unselected style

    def updateStyle(self, isSelected):
        baseStyle = """
            QPushButton {
                border: 1px solid #a9a9a9;
                border-radius: 20px;
                padding: 10px;
                color: black;
                text-align: left;
                padding-left: 20px;
                background-color: #ffffff; /* Default background color is white */
            }
            QPushButton:hover {
                background-color: #e0e0e0; /* Grey color when hovered */
            }
        """
        selectedStyle = "QPushButton { background-color: #F5C754; }"  # Yellow color for the selected button
        
        if isSelected:
            self.setStyleSheet(baseStyle + selectedStyle)
        else:
            self.setStyleSheet(baseStyle)

    def display_details(self):
        # This method will be called when the button is clicked to display the entry details.
        # It will use the display function provided at initialization.
        # Ensure to deselect any previously selected button and select the current one
        self.display_function(self.entry_data, self)