from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QScrollArea, QFormLayout, QSpacerItem, QSizePolicy, QStackedWidget, QTextEdit, QSlider, QCheckBox, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator  # Correct import for QIntValidator
from .Password_Entry import PasswordEntryButton
from core.Password_Generator import PasswordGenerator
import json
from core.utils import get_settings_path
from .Options import OptionsDialog
from ui.ClickableLineEdit import ClickableLineEdit


class VaultWidget(QWidget):
    VAULT_VIEW_INDEX = 0
    ADD_PASSWORD_FORM_INDEX = 1
    PASSWORD_GENERATOR_FORM_INDEX = 2
    def __init__(self, db, settings, themeManager, mainWindow, parent=None):
        super().__init__(parent)
        self.db = db
        self.settings = settings
        self.themeManager = themeManager
        self.mainWindow = mainWindow
        self.selectedButton = None  # Track the selected button in the Vault GUI
        self.encryption_key = None
        self.currentMode = 'all'  # Default mode
        self.current_edit_id = None  # None indicates "add mode"
        self.initUI()
        
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
        # Initialize and add the Add Password Form and Password Generator Form to stackedWidget
        self.init_add_password_form()
        self.init_password_generator_form()
        # Ensure the vault view is the initial view
        self.stackedWidget.setCurrentIndex(self.VAULT_VIEW_INDEX)
        self.applyPasswordVisibility()

    def setupTopBar(self):
        self.topBarLayout = QHBoxLayout()
        titleLabel = QLabel("Credentials Cachers")
        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.setPlaceholderText("Search...")
        self.optionsButton = QPushButton("Options")
        self.optionsButton.clicked.connect(self.showOptionsDialog)
        
        # Connect the textChanged signal to the search_vault method
        self.searchLineEdit.textChanged.connect(self.search_vault)
        
        self.topBarLayout.addWidget(titleLabel)
        self.topBarLayout.addWidget(self.searchLineEdit)
        self.topBarLayout.addWidget(self.optionsButton)
        
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
        self.rightColumnLayout.setSpacing(25)
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
        
        # Use ClickableLineEdit for the password field
        self.passwordLineEdit = ClickableLineEdit()  # Replace QLineEdit with ClickableLineEdit
        self.passwordLineEdit.setMaximumWidth(190)
        self.passwordLineEdit.setReadOnly(True)  # It starts as read-only, clicking will toggle visibility
        # Apply global visibility setting from the start
        self.applyPasswordVisibility()  # Make sure this is defined and updates the visibility based on global settings
        
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
        
        self.lastUpdatedLabel = QLabel("Last Updated: Not available")
        
        # Notes section setup
        notesLayout = QVBoxLayout()
        notesLayout.setSpacing(10)
        notesLabel = QLabel("Notes:")
        notesLayout.addWidget(notesLabel)
        self.notesTextEdit = QTextEdit()
        self.notesTextEdit.setReadOnly(True)
        notesLayout.addWidget(self.notesTextEdit)

        # Add layouts to the right column layout
        self.rightColumnLayout.addLayout(nameRowLayout)
        self.rightColumnLayout.addLayout(usernameRowLayout)
        self.rightColumnLayout.addLayout(passwordRowLayout)
        self.rightColumnLayout.addLayout(sitenameRowLayout)
        self.rightColumnLayout.addWidget(self.lastUpdatedLabel)
        self.rightColumnLayout.addLayout(notesLayout)

        self.mainContentLayout.addLayout(self.rightColumnLayout, 0)

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
        # Add the form widget to the stackedWidget
        self.stackedWidget.addWidget(self.addPasswordFormWidget)
            

    def toggle_add_password_form(self):
        # Define index constants for readability
        ADD_PASSWORD_FORM_INDEX = 1

        currentIndex = self.stackedWidget.currentIndex()
        
        # If we're not already viewing the add password form, switch to it
        if currentIndex != ADD_PASSWORD_FORM_INDEX:
            self.stackedWidget.setCurrentIndex(ADD_PASSWORD_FORM_INDEX)
            self.clear_form_fields()  # Assuming you have a method to clear the form
            self.current_edit_id = None  # Reset to ensure we're in "add mode"
            
    def init_password_generator_form(self):
        self.passwordGeneratorFormWidget = QWidget()  # Ensure this is a QWidget
        generatorLayout = QVBoxLayout()  # Create the layout without passing the widget

        # Initialize UI components as before
        self.generatedPasswordDisplay = QLineEdit()
        self.generatedPasswordDisplay.setReadOnly(True)
        self.generateButton = QPushButton("Generate Password")
        self.lengthSlider = QSlider(Qt.Horizontal)
        self.lengthSlider.setMinimum(12)
        self.lengthSlider.setMaximum(50)
        self.lengthSliderLabel = QLabel("12")
        self.includeUppercaseCheckbox = QCheckBox("Include uppercase letters")
        self.includeNumbersCheckbox = QCheckBox("Include numbers")
        self.includeSpecialCharsCheckbox = QCheckBox("Include special characters")
        self.numbersCountEdit = QLineEdit()
        self.specialCharsCountEdit = QLineEdit()
        self.numbersCountEdit.setValidator(QIntValidator(0, 100))
        self.specialCharsCountEdit.setValidator(QIntValidator(0, 100))

        # Load settings and apply them to the UI components
        pg_settings = self.settings.get("passwordGenerator", {})
        self.lengthSlider.setValue(pg_settings.get("length", 12))
        self.lengthSliderLabel.setText(str(pg_settings.get("length", 12)))  # Update label as well
        self.includeUppercaseCheckbox.setChecked(pg_settings.get("includeUppercase", True))
        self.includeNumbersCheckbox.setChecked(pg_settings.get("includeNumbers", True))
        self.includeSpecialCharsCheckbox.setChecked(pg_settings.get("includeSpecial", True))
        self.numbersCountEdit.setText(str(pg_settings.get("numDigits", 2)))
        self.specialCharsCountEdit.setText(str(pg_settings.get("numSpecial", 2)))

        # Set up the rest of the UI as before
        countsLayout = QHBoxLayout()
        countsLayout.addWidget(QLabel("Number of Digits:"))
        countsLayout.addWidget(self.numbersCountEdit)
        countsLayout.addWidget(QLabel("Number of Special Characters:"))
        countsLayout.addWidget(self.specialCharsCountEdit)
        generatorLayout.addLayout(countsLayout)
        generatorLayout.addWidget(QLabel("Generated Password:"))
        generatorLayout.addWidget(self.generatedPasswordDisplay)
        lengthLayout = QHBoxLayout()
        lengthLayout.addWidget(QLabel("Password Length:"))
        lengthLayout.addWidget(self.lengthSlider)
        lengthLayout.addWidget(self.lengthSliderLabel)
        generatorLayout.addLayout(lengthLayout)
        generatorLayout.addWidget(self.includeUppercaseCheckbox)
        generatorLayout.addWidget(self.includeNumbersCheckbox)
        generatorLayout.addWidget(self.includeSpecialCharsCheckbox)
        generatorLayout.addWidget(self.generateButton)

        # Connect signals
        self.generateButton.clicked.connect(self.generate_password)
        self.lengthSlider.valueChanged.connect(lambda: self.lengthSliderLabel.setText(str(self.lengthSlider.value())))
        self.includeUppercaseCheckbox.stateChanged.connect(self.saveSettingsOnChange)
        self.includeNumbersCheckbox.stateChanged.connect(self.saveSettingsOnChange)
        self.includeSpecialCharsCheckbox.stateChanged.connect(self.saveSettingsOnChange)
        self.numbersCountEdit.textChanged.connect(self.saveSettingsOnChange)
        self.specialCharsCountEdit.textChanged.connect(self.saveSettingsOnChange)
        self.lengthSlider.valueChanged.connect(self.saveSettingsOnChange)

        # Then set the layout on the widget
        self.passwordGeneratorFormWidget.setLayout(generatorLayout)

        # Finally, add the widget to the stackedWidget
        self.stackedWidget.addWidget(self.passwordGeneratorFormWidget)

    def update_slider_value_label(self):
        self.lengthSliderLabel.setText(str(self.lengthSlider.value()))   
                
    def submit_password_details(self):
        self.mainWindow.resetAutoLockTimer()
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
        self.mainWindow.resetAutoLockTimer()
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
            button = PasswordEntryButton(entry, self.themeManager)
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
        self.mainWindow.resetAutoLockTimer()
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
        self.mainWindow.resetAutoLockTimer()
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
        
    def adjustButtonWidth(self):
        """Dynamically adjusts the width of buttons."""
        for layout in [self.leftColumnLayout]:  # Add other layouts as needed
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if isinstance(widget, QPushButton):
                    buttonWidth = int(self.width() * 0.2)
                    widget.setFixedWidth(buttonWidth)

    def resizeEvent(self, event):
        self.mainWindow.resetAutoLockTimer()
        """Handles the widget's resize event and adjusts button widths."""
        self.adjustButtonWidth()
        super().resizeEvent(event)
        
        
    def delete_Entry(self, entry_id):
        self.mainWindow.resetAutoLockTimer()
        print("Deleting entry with ID:", entry_id)
        self.db.delete_password_entry(entry_id)

        # Refresh the vault view. If there's a search term, refresh the search; otherwise, refresh the entire vault.
        if self.searchLineEdit.text():
            self.search_vault()
        else:
            self.populate_vault()
            
    def enter_Edit_Mode(self, entry_data):
        self.mainWindow.resetAutoLockTimer()
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
        self.mainWindow.resetAutoLockTimer()
        new_status = not current_status
        self.db.toggle_favourite_status(entry_id, new_status)
        # Use the currently selected entry's ID to refresh and reselect the entry
        self.populate_vault(reselect_entry_id=entry_id)

    def changeMode(self, mode):
        self.mainWindow.resetAutoLockTimer()
        self.currentMode = mode
        self.populate_vault()
        # Assuming the vault view is at index 0 of the stackedWidget
        self.stackedWidget.setCurrentIndex(0)
        

    def generate_password(self):
        self.mainWindow.resetAutoLockTimer()
        
        length = self.lengthSlider.value()
        include_uppercase = self.includeUppercaseCheckbox.isChecked()
        num_digits = int(self.numbersCountEdit.text())
        num_special = int(self.specialCharsCountEdit.text())
        include_numbers = self.includeNumbersCheckbox.isChecked()
        include_special = self.includeSpecialCharsCheckbox.isChecked()
        

        # Before proceeding with error checking and password generation, save the settings
        settings = {
            "length": length,
            "includeUppercase": include_uppercase,
            "numDigits": num_digits,
            "numSpecial": num_special,
            "includeNumbers": include_numbers,
            "includeSpecial": include_special
        }
        self.savePasswordGeneratorSettings(settings)  # Call the function to save settings

        # Check for errors
        error_messages = []
        if num_digits + num_special > length:
            error_messages.append("Error: Specified digits and special characters exceed total length.")
        if include_numbers and num_digits == 0:
            error_messages.append("Error: Numbers are included, but count is set to 0.")
        if include_special and num_special == 0:
            error_messages.append("Error: Special characters are included, but count is set to 0.")

        # If there are any error messages, display the first one and stop the function
        if error_messages:
            self.displayPasswordOutput(error_messages[0], isError=True)
            return

        # Proceed with generating the password if validation passes
        generated_password = PasswordGenerator.generate_password(length, include_uppercase, num_digits, num_special)
        self.displayPasswordOutput(generated_password, isError=False)


    def saveSettingsOnChange(self):
        # This method will be called whenever a related widget's state changes.
        settings = {
            "length": self.lengthSlider.value(),
            "includeUppercase": self.includeUppercaseCheckbox.isChecked(),
            "numDigits": int(self.numbersCountEdit.text()) if self.numbersCountEdit.text().isdigit() else 0,
            "numSpecial": int(self.specialCharsCountEdit.text()) if self.specialCharsCountEdit.text().isdigit() else 0,
            "includeNumbers": self.includeNumbersCheckbox.isChecked(),
            "includeSpecial": self.includeSpecialCharsCheckbox.isChecked()
        }
        self.mainWindow.resetAutoLockTimer()
        self.savePasswordGeneratorSettings(settings)

    def savePasswordGeneratorSettings(self, settings):
        settings_path = get_settings_path()
        try:
            with open(settings_path, 'r') as file:
                existing_settings = json.load(file)
        except FileNotFoundError:
            existing_settings = {}

        existing_settings["passwordGenerator"] = settings

        with open(settings_path, 'w') as file:
            json.dump(existing_settings, file, indent=4)

    def displayPasswordOutput(self, message, isError=False):
        """
        Displays a message in the generatedPasswordDisplay QLineEdit.
        Adjusts the styling based on whether it's an error message or not.
        """
        if isError:
            # Style for error messages
            self.generatedPasswordDisplay.setStyleSheet("color: red; font-weight: bold;")
        else:
            # Reset to default style for normal password output
            self.generatedPasswordDisplay.setStyleSheet("color: black; font-weight: normal;")

        self.generatedPasswordDisplay.setText(message)
        
    def showOptionsDialog(self):
        optionsDialog = OptionsDialog(self.themeManager, self)
        if optionsDialog.exec_() == QDialog.Accepted:
            self.applyGlobalSettings() 
        
    def applyPasswordVisibility(self):
        # Extract the global setting for password visibility
        show_passwords = self.settings.get('show_passwords', False)

        # Update the visibility setting for all password fields
        self.passwordLineEdit.applyGlobalVisibilitySetting(show_passwords)
        
    def applyGlobalSettings(self):
        # Assuming settings are loaded from a shared settings manager or utility
        self.settings = OptionsDialog.load_or_create_settings()  # Adjust this line accordingly
        self.applyPasswordVisibility()
        
    def showAddPasswordForm(self):
        # Set the current index to show the add password form
        self.stackedWidget.setCurrentIndex(self.ADD_PASSWORD_FORM_INDEX)

