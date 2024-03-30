from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QScrollArea, QFormLayout, QApplication, QFrame, QSpacerItem, QSizePolicy, QStackedWidget
)
from PyQt5.QtCore import Qt

class VaultWidget(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.initUI()

    def initUI(self):
        # Main layout
        self.mainLayout = QVBoxLayout(self)
        
        # Setup sublayouts
        self.setupTopBar()
        self.setupMainContent()

    def setupTopBar(self):
        self.topBarLayout = QHBoxLayout()
        titleLabel = QLabel("Credentials Cachers")
        searchLineEdit = QLineEdit("Search...")
        optionsButton = QPushButton("Options")
        
        self.topBarLayout.addWidget(titleLabel)
        self.topBarLayout.addWidget(searchLineEdit)
        self.topBarLayout.addWidget(optionsButton)
        
        self.mainLayout.addLayout(self.topBarLayout)

    def setupMainContent(self):
        self.mainContentLayout = QHBoxLayout()
        self.setupLeftColumn()
        self.setupCentralColumn()
        self.setupRightColumn()
        
        self.mainLayout.addLayout(self.mainContentLayout)

    def setupLeftColumn(self):
        self.leftColumnLayout = QVBoxLayout()
        allItemsButton = QPushButton("All Items")
        favouritesButton = QPushButton("Favourites")
        passwordGeneratorButton = QPushButton("Password Generator")
        self.add_password_button = QPushButton("Add New Password")  # Define the button here
        self.leftColumnLayout.addWidget(allItemsButton)
        self.leftColumnLayout.addWidget(favouritesButton)
        self.leftColumnLayout.addWidget(passwordGeneratorButton)
        self.leftColumnLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.leftColumnLayout.addWidget(self.add_password_button)
        
        # Connect the add_new_password button to toggle the view
        self.add_password_button.clicked.connect(lambda: self.toggle_add_password_form())
        
        return self.leftColumnLayout

    def setupCentralColumn(self):
        self.centralColumnLayout = QVBoxLayout()
        passwordDisplayArea = QScrollArea()
        passwordDisplayArea.setWidgetResizable(True)
        scrollContent = QWidget()
        scrollContent.setLayout(QVBoxLayout())
        
        passwordDisplayArea.setWidget(scrollContent)
        self.centralColumnLayout.addWidget(passwordDisplayArea)
        
        self.mainContentLayout.addLayout(self.centralColumnLayout)

    def setupRightColumn(self):
        rightColumnLayout = QFormLayout()
        nameLabel = QLabel("Name:")
        nameLineEdit = QLineEdit()
        usernameLabel = QLabel("Username:")
        usernameLineEdit = QLineEdit()
        rightColumnLayout.addRow(nameLabel, nameLineEdit)
        rightColumnLayout.addRow(usernameLabel, usernameLineEdit)
        return rightColumnLayout

    def toggle_view(self, stackedWidget):
        if stackedWidget.currentIndex() == 0:
            stackedWidget.setCurrentIndex(1)
        else:
            stackedWidget.setCurrentIndex(0)

    def init_add_password_form(self):
        # The form now becomes a standalone QWidget that will be added to the stackedWidget
        self.addPasswordFormWidget = QWidget()
        formLayout = QFormLayout(self.addPasswordFormWidget)

        # Initialize form fields
        self.website_name_entry = QLineEdit()
        self.website_url_entry = QLineEdit()
        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.notes_entry = QLineEdit()
        self.submit_button = QPushButton("Submit")

        # Set EchoMode for password entry
        self.password_entry.setEchoMode(QLineEdit.Password)

        # Add widgets to the form layout
        formLayout.addRow("Website Name", self.website_name_entry)
        formLayout.addRow("Website URL", self.website_url_entry)
        formLayout.addRow("Username", self.username_entry)
        formLayout.addRow("Password", self.password_entry)
        formLayout.addRow("Notes", self.notes_entry)
        formLayout.addRow(self.submit_button)

        # Connect the submit button's click signal to the slot that handles the submission
        self.submit_button.clicked.connect(self.submit_password_details)

        # Since this form is meant to be toggled in place of the password display,
        # you would add this widget to the stackedWidget.
        # For simplicity, let's assume `self.stackedWidget` is already defined and is the QStackedWidget
        # that contains both the password display area and the add password form.
        self.stackedWidget.addWidget(self.addPasswordFormWidget)

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
        """Dynamically adjusts the width of buttons."""
        for layout in [self.leftColumnLayout]:  # Add other layouts as needed
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if isinstance(widget, QPushButton):
                    buttonWidth = int(self.width() * 0.2)
                    widget.setFixedWidth(buttonWidth)

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
        """Handles the widget's resize event and adjusts button widths."""
        self.adjustButtonWidth()
        super().resizeEvent(event)
