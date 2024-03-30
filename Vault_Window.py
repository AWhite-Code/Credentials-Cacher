from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QScrollArea, QFormLayout, QApplication, QFrame, QSpacerItem, QSizePolicy, QStackedWidget
)
from PyQt5.QtCore import Qt
from Password_Entry import PasswordEntryButton

class VaultWidget(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.selectedButton = None  # Track the selected button
        self.initUI()

    def initUI(self):
        # Main layout
        self.mainLayout = QVBoxLayout(self)
        # Setup sublayouts
        self.setupTopBar()
        self.setupMainContent()
        self.applyStylesheet()
        self.stackedWidget.setCurrentIndex(0)

    def setupTopBar(self):
        self.topBarLayout = QHBoxLayout()
        titleLabel = QLabel("Credentials Cachers")
        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.setPlaceholderText("Search...")
        optionsButton = QPushButton("Options")
        
        # Connect the textChanged signal to the search_vault method
        self.searchLineEdit.textChanged.connect(self.search_vault)
        
        self.topBarLayout.addWidget(titleLabel)
        self.topBarLayout.addWidget(self.searchLineEdit)
        self.topBarLayout.addWidget(optionsButton)
        
        self.mainLayout.addLayout(self.topBarLayout)

    def setupMainContent(self):
        self.mainContentLayout = QHBoxLayout()
        self.stackedWidget = QStackedWidget()  # This will toggle between the vault and the add password form

        # Setup columns
        self.setupLeftColumn()
        self.setupCentralColumn()  # Modify this to add the vault view and the add password form to stackedWidget
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
       
        self.mainContentLayout.addLayout(self.leftColumnLayout, 0)
            
    def setupCentralColumn(self):
        self.centralColumnLayout = QVBoxLayout()

        # Initialize the QStackedWidget
        self.stackedWidget = QStackedWidget()

        # Set up the password display area
        passwordDisplayArea = QScrollArea()
        passwordDisplayArea.setWidgetResizable(True)
        scrollContent = QWidget()
        self.scrollContentLayout = QVBoxLayout(scrollContent)  # Use self to make it accessible elsewhere
        self.scrollContentLayout.setAlignment(Qt.AlignTop)  # Ensure content starts from the top

        passwordDisplayArea.setStyleSheet("QScrollArea { border: none; } QScrollArea > QWidgetViewport { border: none; }")
        passwordDisplayArea.setWidget(scrollContent)

        # Add the password display area (vault view) to stackedWidget as the first view
        self.stackedWidget.addWidget(passwordDisplayArea)

        # Call init_add_password_form to setup and add the Add Password Form as the second view
        self.init_add_password_form()

        # Ensure the vault view is the initial view
        self.stackedWidget.setCurrentIndex(0)

        # Add the stackedWidget to the central column layout
        self.centralColumnLayout.addWidget(self.stackedWidget)

        # Finally, add the centralColumnLayout to the main content layout
        self.mainContentLayout.addLayout(self.centralColumnLayout, 1)

        # Populate the vault
        self.populate_vault()
            
    def init_add_password_form(self):
        self.addPasswordFormWidget = QWidget()
        formLayout = QFormLayout(self.addPasswordFormWidget)
        # Set up form fields...
        self.stackedWidget.addWidget(self.addPasswordFormWidget)


    def setupRightColumn(self):
        self.rightColumnLayout = QVBoxLayout()

        # Explicitly setting spacing and margins to see immediate effects
        self.rightColumnLayout.setSpacing(50)  # Adjust this value as needed
        self.rightColumnLayout.setContentsMargins(10, 10, 10, 10)

        # Name row setup
        nameRowLayout = QHBoxLayout()
        nameLabel = QLabel("Name:")
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setMaximumWidth(160)
        self.nameLineEdit.setReadOnly(True)
        nameRowLayout.addWidget(nameLabel)
        nameRowLayout.addWidget(self.nameLineEdit)

        # Username row setup
        usernameRowLayout = QHBoxLayout()
        usernameLabel = QLabel("Username:")
        self.usernameLineEdit = QLineEdit()
        self.usernameLineEdit.setMaximumWidth(300)
        self.usernameLineEdit.setReadOnly(True)
        usernameRowLayout.addWidget(usernameLabel)
        usernameRowLayout.addWidget(self.usernameLineEdit)

        # Password row setup
        passwordRowLayout = QHBoxLayout()
        passwordLabel = QLabel("Password:")
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setMaximumWidth(190)
        self.passwordLineEdit.setReadOnly(True)
        passwordRowLayout.addWidget(passwordLabel)
        passwordRowLayout.addWidget(self.passwordLineEdit)

        # Website Address row setup
        sitenameRowLayout = QHBoxLayout()
        sitenameLabel = QLabel("Website:")
        self.sitenameLineEdit = QLineEdit()
        self.sitenameLineEdit.setMaximumWidth(160)
        self.sitenameLineEdit.setReadOnly(True)
        sitenameRowLayout.addWidget(sitenameLabel)
        sitenameRowLayout.addWidget(self.sitenameLineEdit)

        # Adding row layouts to the right column layout
        self.rightColumnLayout.addLayout(nameRowLayout)
        self.rightColumnLayout.addLayout(usernameRowLayout)
        self.rightColumnLayout.addLayout(passwordRowLayout)
        self.rightColumnLayout.addLayout(sitenameRowLayout)

        # Add stretch to push all content to the top
        self.rightColumnLayout.addStretch(1)

        # Now add the rightColumnLayout to the main content layout
        self.mainContentLayout.addLayout(self.rightColumnLayout, 0)
        

    def toggle_view(self, stackedWidget):
        if stackedWidget.currentIndex() == 0:
            stackedWidget.setCurrentIndex(1)
        else:
            stackedWidget.setCurrentIndex(0)

    def init_add_password_form(self):
        self.addPasswordFormWidget = QWidget()
        # Create a QVBoxLayout for the form widget
        verticalLayout = QVBoxLayout(self.addPasswordFormWidget)
        
        # Create a spacer item with a small height (e.g., 10 pixels) and add it to the vertical layout
        spacer = QSpacerItem(20, 150, QSizePolicy.Minimum, QSizePolicy.Fixed)
        verticalLayout.addSpacerItem(spacer)
        
        # Now create the form layout and add your form fields to this layout
        formLayout = QFormLayout()
        # Initialize form fields...
        self.website_name_entry = QLineEdit()
        self.website_url_entry = QLineEdit()
        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.notes_entry = QLineEdit()
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_password_details)

        # Add widgets to the form layout
        formLayout.addRow("Website Name", self.website_name_entry)
        formLayout.addRow("Website URL", self.website_url_entry)
        formLayout.addRow("Username", self.username_entry)
        formLayout.addRow("Password", self.password_entry)
        formLayout.addRow("Notes", self.notes_entry)
        formLayout.addRow(self.submit_button)
        
        # Add the form layout to the vertical layout
        verticalLayout.addLayout(formLayout)

        # Adjust the spacing of the form layout if needed
        formLayout.setSpacing(50)

        # Add the form widget to the stackedWidget
        self.stackedWidget.addWidget(self.addPasswordFormWidget)

    def toggle_add_password_form(self):
        # Toggle between the vault view and the Add Password form
        currentIndex = self.stackedWidget.currentIndex()
        if currentIndex == 0:
            self.stackedWidget.setCurrentIndex(1)  # Show Add Password form
        else:
            self.stackedWidget.setCurrentIndex(0)  # Show vault view

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
        
        self.populate_vault()

    def clear_form_fields(self):
        """Clears all input fields in the form."""
        self.website_name_entry.clear()
        self.website_url_entry.clear()
        self.username_entry.clear()
        self.password_entry.clear()
        self.notes_entry.clear()
    
    def populate_vault(self, entries=None):
        if entries is None:
            entries = self.db.fetch_all_entries()
        
        # Clear existing content in the vault display area
        while self.scrollContentLayout.count():
            child = self.scrollContentLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add filtered or all entries to the vault
        for entry in entries:
            button = PasswordEntryButton(entry, self.display_entry_details)
            self.scrollContentLayout.addWidget(button)
            
    def search_vault(self):
        search_query = self.searchLineEdit.text().lower()
        all_entries = self.db.fetch_all_entries()
        filtered_entries = [entry for entry in all_entries if search_query in entry[1].lower()]

        self.populate_vault(filtered_entries)


    def display_entry_details(self, entry_data, button):
        if self.selectedButton:
            self.selectedButton.updateStyle(False)  # Deselect the previous button
        self.selectedButton = button  # Update the selected button
        self.selectedButton.updateStyle(True)  # Highlight the new button

        # Proceed to set the entry data in the right column QLineEdit widgets
        # This part remains unchanged
        self.nameLineEdit.setText(entry_data[1])
        self.sitenameLineEdit.setText(entry_data[2])
        self.usernameLineEdit.setText(entry_data[3])
        self.passwordLineEdit.setText(entry_data[4])

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
        
    def adjustButtonWidth(self):
        """Dynamically adjusts the width of buttons."""
        for layout in [self.leftColumnLayout]:  # Add other layouts as needed
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if isinstance(widget, QPushButton):
                    buttonWidth = int(self.width() * 0.2)
                    widget.setFixedWidth(buttonWidth)

    def resizeEvent(self, event):
        """Handles the widget's resize event and adjusts button widths."""
        self.adjustButtonWidth()
        super().resizeEvent(event)
