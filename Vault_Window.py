from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QScrollArea, QFormLayout, QSpacerItem, QSizePolicy, QStackedWidget, QTextEdit, QFrame, QSlider, QCheckBox
)
from PyQt5.QtCore import Qt
from Password_Entry import PasswordEntryButton
from Password_Generator import PasswordGenerator

class VaultWidget(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.selectedButton = None  # Track the selected button
        self.encryption_key = None
        self.currentMode = 'all'  # Default mode
        self.initUI()
        self.current_edit_id = None  # None indicates "add mode"
        
    def set_encryption_key(self, key):
        self.encryption_key = key
        if key is not None:
            self.populate_vault()  

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

        # Layout for vault ordering buttons
        vaultOrderLayout = QVBoxLayout()
        orderLabel = QLabel("Order vault by:")
        vaultOrderLayout.addWidget(orderLabel)

        allItemsButton = QPushButton("All Items")
        allItemsButton.clicked.connect(lambda: self.changeMode('all'))
        vaultOrderLayout.addWidget(allItemsButton)
            
        favouritesButton = QPushButton("Favourites")
        favouritesButton.clicked.connect(lambda: self.changeMode('favourites'))
        vaultOrderLayout.addWidget(favouritesButton)
        
        alphabeticalOrderButton = QPushButton("Alphabetical Order")
        alphabeticalOrderButton.clicked.connect(lambda: self.changeMode('alphabetical'))
        vaultOrderLayout.addWidget(alphabeticalOrderButton)

        lastUpdatedButton = QPushButton("Last Updated")
        lastUpdatedButton.clicked.connect(lambda: self.changeMode('lastUpdated'))
        vaultOrderLayout.addWidget(lastUpdatedButton)

        # Add vault ordering layout to the main left column layout
        self.leftColumnLayout.addLayout(vaultOrderLayout)

        # Spacer after vault ordering
        self.leftColumnLayout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Password Generator button
        passwordGeneratorButton = QPushButton("Password Generator")
        self.leftColumnLayout.addWidget(passwordGeneratorButton)
        passwordGeneratorButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.passwordGeneratorFormWidget)))

        # Spacer before the Add New Password button
        self.leftColumnLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add New Password button at the bottom
        self.add_password_button = QPushButton("Add New Password")
        self.add_password_button.clicked.connect(lambda: self.toggle_add_password_form())
        self.leftColumnLayout.addWidget(self.add_password_button)

        # Add the left column layout to the main content layout at the leftmost position
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
        
        self.init_password_generator_form()

        # Ensure the vault view is the initial view
        self.stackedWidget.setCurrentIndex(0)

        # Add the stackedWidget to the central column layout
        self.centralColumnLayout.addWidget(self.stackedWidget)

        # Finally, add the centralColumnLayout to the main content layout
        self.mainContentLayout.addLayout(self.centralColumnLayout, 1)

        # Populate the vault
        self.populate_vault()


    def setupRightColumn(self):
        self.rightColumnLayout = QVBoxLayout()

        # Explicitly setting spacing and margins for overall right column layout
        self.rightColumnLayout.setSpacing(25)  # Adjust this value as needed for space between different rows
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
        
        self.lastUpdatedLabel = QLabel("Last Updated: Not available")  # Initial text

        # Notes section setup, with minimized spacing between label and text edit
        notesLayout = QVBoxLayout()
        notesLayout.setSpacing(10)  # No space between the label and the text edit
        notesLabel = QLabel("Notes:")
        notesLayout.addWidget(notesLabel)
        self.notesTextEdit = QTextEdit()
        self.notesTextEdit.setReadOnly(True)
        notesLayout.addWidget(self.notesTextEdit)

        # Adding row layouts and the notes section layout to the right column layout
        self.rightColumnLayout.addLayout(nameRowLayout)
        self.rightColumnLayout.addLayout(usernameRowLayout)
        self.rightColumnLayout.addLayout(passwordRowLayout)
        self.rightColumnLayout.addLayout(sitenameRowLayout)
        self.rightColumnLayout.addWidget(self.lastUpdatedLabel)
        self.rightColumnLayout.addLayout(notesLayout)

        # This stretch is removed to allow the notesTextEdit to take the remaining space.
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
            
    def init_password_generator_form(self):
        self.passwordGeneratorFormWidget = QWidget()
        formLayout = QVBoxLayout(self.passwordGeneratorFormWidget)
        
        # Length Slider
        self.lengthSlider = QSlider(Qt.Horizontal)
        self.lengthSlider.setMinimum(12)
        self.lengthSlider.setMaximum(50)
        self.lengthSlider.setValue(12)
        
        # Length Label
        lengthLabel = QLabel("Password Length: 12")
        self.lengthSlider.valueChanged.connect(lambda: lengthLabel.setText(f"Password Length: {self.lengthSlider.value()}"))
        
        # Generate Button
        generateButton = QPushButton("Generate Password")
        generateButton.clicked.connect(self.generate_password)
        
        # Password Display
        self.generatedPasswordDisplay = QLineEdit()
        self.generatedPasswordDisplay.setReadOnly(True)

        # Add widgets to the form layout
        formLayout.addWidget(lengthLabel)
        formLayout.addWidget(self.lengthSlider)
        formLayout.addWidget(generateButton)
        formLayout.addWidget(self.generatedPasswordDisplay)
        
        # Add the form widget to the stackedWidget
        self.stackedWidget.addWidget(self.passwordGeneratorFormWidget)      
                
    def submit_password_details(self):
        """Handles the submission of password details for both adding new and updating existing entries."""
        website_name = self.website_name_entry.text()
        website_url = self.website_url_entry.text()
        username = self.username_entry.text()
        password = self.password_entry.text()
        notes = self.notes_entry.text()

        # Ensure that the encryption key is available before proceeding
        if self.encryption_key is not None:
            try:
                if self.current_edit_id is not None:
                    # Update existing entry
                    self.db.update_password_entry(self.current_edit_id, website_name, website_url, username, password, notes, self.encryption_key)
                    print("Entry updated successfully.")
                else:
                    # Add new entry
                    self.db.add_password_entry(website_name, website_url, username, password, notes, self.encryption_key)
                    print("Entry added successfully.")

                # Clear form fields and refresh the vault display, toggling back to the vault view
                self.clear_form_fields()
                self.populate_vault()
                self.stackedWidget.setCurrentIndex(0)  # Assumes the vault view is at index 0
            except Exception as e:
                # Log the error or inform the user about the failure
                print(f"Failed to process entry: {e}")
        else:
            # Handle the scenario where the encryption key is not available
            print("Encryption key is not available. Cannot process the entry.")

        # Reset the current_edit_id to None to ensure the form is back in "add mode"
        self.current_edit_id = None


    def clear_form_fields(self):
        """Clears all input fields in the form."""
        self.website_name_entry.clear()
        self.website_url_entry.clear()
        self.username_entry.clear()
        self.password_entry.clear()
        self.notes_entry.clear()
    
    def populate_vault(self, entries=None, reselect_entry_id=None):
        """Fetch and display entries using the current encryption key."""
        if self.selectedButton:
            self.selectedButton.setSelected(False)
            self.selectedButton = None

        while self.scrollContentLayout.count():
            child = self.scrollContentLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if entries is None:
            if self.currentMode == 'all':
                entries = self.db.fetch_all_entries(self.encryption_key)
            elif self.currentMode == 'favourites':
                entries = self.db.fetch_favourites(self.encryption_key)
            elif self.currentMode == 'alphabetical':
                entries = sorted(self.db.fetch_all_entries(self.encryption_key), key=lambda x: x[1].lower())
            elif self.currentMode == 'lastUpdated':
                entries = sorted(self.db.fetch_all_entries(self.encryption_key), key=lambda x: x[7], reverse=True)

        for entry in entries:
            button = PasswordEntryButton(entry)
            button.displayDetails.connect(lambda entry_data=entry, button=button: self.display_entry_details(entry_data, button))
            button.editClicked.connect(lambda entry_data=entry: self.enter_Edit_Mode(entry_data))
            button.deleteClicked.connect(lambda: self.delete_Entry(entry[0]))
            button.toggleFavourite.connect(self.handleToggleFavourite)
            self.scrollContentLayout.addWidget(button)
            
            # Reselect the entry if it matches the reselect_entry_id
            if reselect_entry_id is not None and entry[0] == reselect_entry_id:
                self.display_entry_details(entry, button)
                button.setSelected(True)
                self.selectedButton = button
                
    def search_vault(self):
        """Filter and display entries based on the search query using the current encryption key."""
        if not self.encryption_key:
            self.populate_vault([])  # Clear the display if there's no encryption key
            return  # Guard clause to exit early if there's no encryption key

        search_query = self.searchLineEdit.text().lower()
        print(f"Search query: {search_query}")
        # Decide which set of entries to fetch based on the current mode
        if self.currentMode == 'all':
            all_entries = self.db.fetch_all_entries(self.encryption_key)
        else:  # 'favourites' mode
            all_entries = self.db.fetch_favourites(self.encryption_key)

        # Debug: Print all entries fetched before filtering
        print(f"All entries before filtering: {[entry[1] for entry in all_entries]}")

        # Filter the entries based on the search query
        filtered_entries = [entry for entry in all_entries if search_query in entry[1].lower()]

        # Debug: Print entries after filtering
        print(f"Filtered entries: {[entry[1] for entry in filtered_entries]}")

        self.populate_vault(filtered_entries)


    def display_entry_details(self, entry_data, button):
        # Deselect the previously selected button, if any
        if self.selectedButton is not None:
            # Ensure the previously selected button's style is reset
            self.selectedButton.setSelected(False)

        # Update the selectedButton reference to the new button
        self.selectedButton = button
        # Mark the new button as selected
        self.selectedButton.setSelected(True)

        # Set the entry details in the UI based on entry_data
        self.nameLineEdit.setText(entry_data[1])
        self.sitenameLineEdit.setText(entry_data[2] if len(entry_data) > 2 else "")
        self.usernameLineEdit.setText(entry_data[3] if len(entry_data) > 3 else "")
        self.passwordLineEdit.setText(entry_data[4] if len(entry_data) > 4 else "")
        self.notesTextEdit.setText(entry_data[5] if len(entry_data) > 5 else "")
        self.lastUpdatedLabel.setText(f"Last Updated: {entry_data[8]}" if len(entry_data) > 8 else "")

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
                background-color: #F5C754;
                color: black;
                outline: none;
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
        
        
    def delete_Entry(self, entry_id):
        print("Deleting entry with ID:", entry_id)
        self.db.delete_password_entry(entry_id)

        # Refresh the vault view. If there's a search term, refresh the search; otherwise, refresh the entire vault.
        if self.searchLineEdit.text():
            self.search_vault()
        else:
            self.populate_vault()
            
    def enter_Edit_Mode(self, entry_data):
        print("Entering edit mode for entry:", entry_data[0])
        """Prepares and shows the add/edit form with pre-filled entry data for editing."""
        self.website_name_entry.setText(entry_data[1])
        self.website_url_entry.setText(entry_data[2])
        self.username_entry.setText(entry_data[3])
        self.password_entry.setText(entry_data[4])
        self.notes_entry.setText(entry_data[5])
        # Assuming entry_data[0] is the ID
        self.current_edit_id = entry_data[0]
        # Switch to the add/edit form view
        self.stackedWidget.setCurrentIndex(1)
        
    def handleToggleFavourite(self, entry_id, current_status):
        new_status = not current_status
        self.db.toggle_favourite_status(entry_id, new_status)
        # Use the currently selected entry's ID to refresh and reselect the entry
        self.populate_vault(reselect_entry_id=entry_id)

    def changeMode(self, mode):
        self.currentMode = mode
        self.populate_vault()
        
    def generate_password(self):
        length = self.lengthSlider.value()
        generated_password = PasswordGenerator.generate_password(length)
        self.generatedPasswordDisplay.setText(generated_password)