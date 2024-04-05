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
    """
    The main widget for displaying the vault where password entries are listed.
    It allows for adding, editing, and deleting password entries, generating passwords,
    and switching between different viewing modes of the vault.
    """

    # Define constants for the index of different views within the QStackedWidget
    VAULT_VIEW_INDEX = 0
    ADD_PASSWORD_FORM_INDEX = 1
    PASSWORD_GENERATOR_FORM_INDEX = 2

    def __init__(self, db, settings, themeManager, mainWindow, parent=None):
        """
        Initializes the VaultWidget with connections to the database, application settings,
        theme manager, and the main application window.

        :param db: Database connection object.
        :param settings: Application settings loaded from a JSON file.
        :param themeManager: Manages the application's themes.
        :param mainWindow: Reference to the main application window.
        :param parent: Parent widget, defaults to None.
        """
        super().__init__(parent)
        self.db = db
        self.settings = settings
        self.themeManager = themeManager
        self.mainWindow = mainWindow
        self.selectedButton = None  # Track the selected button in the Vault GUI
        self.encryption_key = None  # Encryption key for encrypting/decrypting entries
        self.currentMode = 'all'  # Default mode for displaying entries
        self.current_edit_id = None  # Track the ID of the entry being edited, None for adding new
        self.initUI()

    def set_encryption_key(self, key):
        """
        Sets the encryption key for the session and populates the vault with entries.

        :param key: The encryption key used for decrypting password entries.
        """
        self.encryption_key = key
        if key is not None:
            self.populate_vault()

    def initUI(self):
        """
        Initializes the user interface, setting up the layout, top bar, main content area,
        and ensuring the initial view is set correctly.
        """
        # Main layout setup
        self.mainLayout = QVBoxLayout(self)

        # Setup sublayouts for different sections of the UI
        self.setupTopBar()
        self.setupMainContent()

        # Initialize forms for adding passwords and generating passwords, adding them to the stacked widget
        self.init_add_password_form()
        self.init_password_generator_form()

        # Set the initial view to the vault view
        self.stackedWidget.setCurrentIndex(self.VAULT_VIEW_INDEX)

        # Apply global password visibility settings
        self.applyPasswordVisibility()

    def setupTopBar(self):
        """
        Sets up the top bar of the vault UI, including the application title,
        search field, and options button.
        """
        # Top bar layout and components
        self.topBarLayout = QHBoxLayout()
        titleLabel = QLabel("Credentials Cachers")
        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.setPlaceholderText("Search...")
        self.optionsButton = QPushButton("Options")
        self.optionsButton.clicked.connect(self.showOptionsDialog)

        # Connect search line edit changes to the search_vault method
        self.searchLineEdit.textChanged.connect(self.search_vault)

        # Add components to the top bar layout
        self.topBarLayout.addWidget(titleLabel)
        self.topBarLayout.addWidget(self.searchLineEdit)
        self.topBarLayout.addWidget(self.optionsButton)

        # Add top bar layout to the main layout
        self.mainLayout.addLayout(self.topBarLayout)

    def setupMainContent(self):
        """
        Sets up the main content area of the vault UI, including left, central,
        and right columns for different functionalities and views.
        """
        self.mainContentLayout = QHBoxLayout()

        # Stacked widget to switch between vault view, add password form, and password generator form
        self.stackedWidget = QStackedWidget()

        # Setup each column in the main content area
        self.setupLeftColumn()
        self.setupCentralColumn()
        self.setupRightColumn()
        
        # Inside setupMainContent, after setting up columns
        self.mainContentLayout.addLayout(self.leftColumnLayout, 1)  # Left column
        self.mainContentLayout.addWidget(self.stackedWidget, 3)     # Central column with stackedWidget
        self.mainContentLayout.addLayout(self.rightColumnLayout, 1) # Right colum

        # Add the main content layout to the main layout of the widget
        self.mainLayout.addLayout(self.mainContentLayout)

    def setupLeftColumn(self):
        """
        Sets up the left column of the main content area, which includes
        buttons for changing the vault view and accessing the password generator.
        """
        self.leftColumnLayout = QVBoxLayout()

        # Layout for buttons to order and filter the vault entries
        vaultOrderLayout = QVBoxLayout()
        orderLabel = QLabel("Order vault by:")
        vaultOrderLayout.addWidget(orderLabel)

        # Buttons for different sorting and filtering modes
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

        # Add the ordering layout to the left column layout
        self.leftColumnLayout.addLayout(vaultOrderLayout)

        # Spacer items for layout management
        self.leftColumnLayout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Button to access the password generator
        passwordGeneratorButton = QPushButton("Password Generator")
        passwordGeneratorButton.clicked.connect(self.showPasswordGeneratorForm)
        self.leftColumnLayout.addWidget(passwordGeneratorButton)

        self.leftColumnLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Button to add a new password entry
        self.add_password_button = QPushButton("Add New Password")
        self.add_password_button.clicked.connect(self.toggle_add_password_form)
        self.leftColumnLayout.addWidget(self.add_password_button)

            
    def setupCentralColumn(self):
        """
        Sets up the central column of the vault's main UI. This method initializes
        a QStackedWidget which will contain the vault's entry display area and forms for adding
        or editing entries, enabling easy switching between these views.
        """
        self.centralColumnLayout = QVBoxLayout()

        # Initialize the QStackedWidget to switch between different views
        self.stackedWidget = QStackedWidget()

        # Create a scroll area for displaying password entries
        passwordDisplayArea = QScrollArea()
        passwordDisplayArea.setWidgetResizable(True)
        scrollContent = QWidget()
        self.scrollContentLayout = QVBoxLayout(scrollContent)
        self.scrollContentLayout.setAlignment(Qt.AlignTop)

        # Set styles for the scroll area to remove border
        passwordDisplayArea.setStyleSheet("QScrollArea { border: none; } QScrollArea > QWidgetViewport { border: none; }")
        passwordDisplayArea.setWidget(scrollContent)

        # Add the password display area to the stacked widget as the initial view
        self.stackedWidget.addWidget(passwordDisplayArea)

        # Set the vault view as the initial view
        self.stackedWidget.setCurrentIndex(0)

        # Add the stacked widget to the central column layout
        self.centralColumnLayout.addWidget(self.stackedWidget)

        # Populate the vault with entries
        self.populate_vault()

    def setupRightColumn(self):
        """
        Sets up the right column for displaying selected password entry details.
        It includes read-only fields for the entry's name, username, password,
        website, last updated timestamp, and notes.
        """
        self.rightColumnLayout = QVBoxLayout()
        self.rightColumnLayout.setSpacing(25)
        self.rightColumnLayout.setContentsMargins(10, 10, 10, 10)

        # Initialize detail QLineEdit widgets here
        self.nameLineEdit = QLineEdit()
        self.usernameLineEdit = QLineEdit()
        self.passwordLineEdit = ClickableLineEdit()  # Assuming ClickableLineEdit is a subclass of QLineEdit
        self.sitenameLineEdit = QLineEdit()
        self.notesTextEdit = QTextEdit()

        # Make line edits read-only
        for lineEdit in [self.nameLineEdit, self.usernameLineEdit, self.passwordLineEdit, self.sitenameLineEdit]:
            lineEdit.setReadOnly(True)
        
        # If password visibility toggle functionality exists, set passwordLineEdit as clickable
        self.passwordLineEdit.setCursor(Qt.PointingHandCursor)  # Only necessary if ClickableLineEdit doesn't set this by default
        self.applyPasswordVisibility()  # Assuming this method correctly applies the visibility state

        # Create row layouts for each detail
        nameRowLayout = self.createDetailRow("Name:", self.nameLineEdit, 80)
        usernameRowLayout = self.createDetailRow("Username:", self.usernameLineEdit, 80)
        passwordRowLayout = self.createDetailRow("Password:", self.passwordLineEdit, 80, isClickable=True)
        sitenameRowLayout = self.createDetailRow("Website:", self.sitenameLineEdit, 80)
        self.lastUpdatedLabel = QLabel("Last Updated: Not available")

        # Setup Notes section
        notesLayout = self.setupNotesSection()

        # Add rows and sections to the right column layout
        self.rightColumnLayout.addLayout(nameRowLayout)
        self.rightColumnLayout.addLayout(usernameRowLayout)
        self.rightColumnLayout.addLayout(passwordRowLayout)
        self.rightColumnLayout.addLayout(sitenameRowLayout)
        self.rightColumnLayout.addWidget(self.lastUpdatedLabel)
        self.rightColumnLayout.addLayout(notesLayout)

    def setupNotesSection(self):
        """
        Creates the layout for the notes section.
        """
        notesLayout = QVBoxLayout()
        notesLayout.setSpacing(10)
        notesLabel = QLabel("Notes:")
        self.notesTextEdit.setReadOnly(True)
        notesLayout.addWidget(notesLabel)
        notesLayout.addWidget(self.notesTextEdit)
        return notesLayout

    def createDetailRow(self, label, lineEdit, maxWidth, isClickable=False):
        """
        Creates a row layout for displaying a detail of the selected password entry.

        :param label: The text label for the detail.
        :param lineEdit: The QLineEdit widget used to display the detail value.
        :param maxWidth: The maximum width of the QLineEdit widget.
        :param isClickable: A flag indicating if the QLineEdit widget should be clickable. Defaults to False.
        :return: The QHBoxLayout instance containing the label and QLineEdit widgets.
        """
        rowLayout = QHBoxLayout()
        detailLabel = QLabel(label)
        lineEdit.setMaximumWidth(maxWidth)
        lineEdit.setReadOnly(True)
        
        # Apply ClickableLineEdit specific properties if isClickable is True
        if isClickable:
            lineEdit.setCursor(Qt.PointingHandCursor)
            self.applyPasswordVisibility()

        rowLayout.addWidget(detailLabel)
        rowLayout.addWidget(lineEdit)
        return rowLayout

    def init_add_password_form(self):
        """
        Initializes the form for adding a new password entry. This form allows users
        to input details about a site or service, including its name, URL, username,
        password, and any additional notes. A submit button is included to save the entry.
        """
        self.addPasswordFormWidget = QWidget()  # Create the container widget for the form
        verticalLayout = QVBoxLayout(self.addPasswordFormWidget)  # Arrange form elements vertically

        # Add a spacer to create vertical space at the beginning of the form
        spacer = QSpacerItem(20, 150, QSizePolicy.Minimum, QSizePolicy.Fixed)
        verticalLayout.addSpacerItem(spacer)

        formLayout = QFormLayout()  # Organize form fields and labels in a two-column layout
        # Initialize and add input fields and labels to the form
        self.website_name_entry = QLineEdit()
        self.website_url_entry = QLineEdit()
        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.notes_entry = QLineEdit()
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_password_details)  # Connect submit action

        # Add each form field to the form layout
        formLayout.addRow("Website Name", self.website_name_entry)
        formLayout.addRow("Website URL", self.website_url_entry)
        formLayout.addRow("Username", self.username_entry)
        formLayout.addRow("Password", self.password_entry)
        formLayout.addRow("Notes", self.notes_entry)
        formLayout.addRow(self.submit_button)

        verticalLayout.addLayout(formLayout)  # Add the form layout to the vertical layout
        self.stackedWidget.addWidget(self.addPasswordFormWidget)  # Add the form widget to the stacked widget

    def toggle_add_password_form(self):
        """
        Toggles the view to the add password form within the stacked widget.
        Clears any existing input in the form fields and ensures the form is in 'add' mode.
        """
        ADD_PASSWORD_FORM_INDEX = 1  # Index of the add password form within the stacked widget

        if self.stackedWidget.currentIndex() != ADD_PASSWORD_FORM_INDEX:
            # Switch to the add password form and clear any existing inputs
            self.stackedWidget.setCurrentIndex(ADD_PASSWORD_FORM_INDEX)
            self.clear_form_fields()
            self.current_edit_id = None  # Reset to indicate a new entry is being added

    def init_password_generator_form(self):
        """
        Initializes the password generator form with a detailed layout. The form includes a title label,
        a display for the generated password, a slider for selecting password length with a dynamic label 
        showing its value, options to specify the number of special characters and numbers, and checkboxes 
        for including uppercase letters, special characters, and numbers.
        """
        self.passwordGeneratorFormWidget = QWidget()  # The container widget for the form
        generatorLayout = QVBoxLayout()  # Layout to arrange UI components vertically

        # Title label for the password generator section
        passwordGeneratorTitle = QLabel("Password Generator:")
        passwordGeneratorTitle.setAlignment(Qt.AlignCenter)  # Center the title above the password box
        generatorLayout.addWidget(passwordGeneratorTitle)

        # Display for the generated password
        self.generatedPasswordDisplay = QLineEdit()  # Display generated password
        self.generatedPasswordDisplay.setReadOnly(True)  # Make display read-only
        generatorLayout.addWidget(self.generatedPasswordDisplay)

        # Label and slider for password length
        passwordLengthLayout = QHBoxLayout()
        passwordLengthLabel = QLabel("Password length: ")
        self.lengthSliderLabel = QLabel("12")  # Initial value of the slider
        self.lengthSlider = QSlider(Qt.Horizontal)  # Slider to select password length
        self.lengthSlider.setMinimum(12)  # Minimum length
        self.lengthSlider.setMaximum(50)  # Maximum length
        self.lengthSlider.valueChanged.connect(lambda value: self.lengthSliderLabel.setText(str(value)))
        passwordLengthLayout.addWidget(passwordLengthLabel)
        passwordLengthLayout.addWidget(self.lengthSlider)
        passwordLengthLayout.addWidget(self.lengthSliderLabel)
        generatorLayout.addLayout(passwordLengthLayout)

        # Checkboxes for password criteria
        self.includeUppercaseCheckbox = QCheckBox("Include uppercase letters")
        generatorLayout.addWidget(self.includeUppercaseCheckbox)
        self.includeSpecialCharsCheckbox = QCheckBox("Include special characters")
        generatorLayout.addWidget(self.includeSpecialCharsCheckbox)
        self.includeNumbersCheckbox = QCheckBox("Include numbers")
        generatorLayout.addWidget(self.includeNumbersCheckbox)
        
        # Checkboxes are set to True by default
        self.includeUppercaseCheckbox.setChecked(True)
        self.includeNumbersCheckbox.setChecked(True)
        self.includeSpecialCharsCheckbox.setChecked(True)

        # LineEdits for specifying the number of digits and special characters, with labels
        numbersAndSpecialCharsLayout = QHBoxLayout()
        self.specialCharsCountEdit = QLineEdit()
        self.specialCharsCountEdit.setText("1")
        self.specialCharsCountEdit.setValidator(QIntValidator(0, 100))  # Ensure only numeric input
        self.numbersCountEdit = QLineEdit()
        self.numbersCountEdit.setText("1")
        self.numbersCountEdit.setValidator(QIntValidator(0, 100))  # Ensure only numeric input
        numbersAndSpecialCharsLayout.addWidget(QLabel("Special Characters amount:"))
        numbersAndSpecialCharsLayout.addWidget(self.specialCharsCountEdit)
        numbersAndSpecialCharsLayout.addWidget(QLabel("Numbers amount:"))
        numbersAndSpecialCharsLayout.addWidget(self.numbersCountEdit)
        generatorLayout.addLayout(numbersAndSpecialCharsLayout)

        # Button to trigger password generation
        self.generateButton = QPushButton("Generate Password")
        generatorLayout.addWidget(self.generateButton)

        # Set the layout on the form widget
        self.passwordGeneratorFormWidget.setLayout(generatorLayout)

        # Add the password generator form widget to the stacked widget
        self.stackedWidget.addWidget(self.passwordGeneratorFormWidget)
        self.connectPasswordGeneratorSignals()
        
    def layoutPasswordGeneratorForm(self, generatorLayout):
        """
        Arranges the UI components of the password generator form within the given layout.
        
        :param generatorLayout: The QVBoxLayout instance to which the form components should be added.
        """
        # Arrange components for number of digits and special characters in a horizontal layout
        countsLayout = QHBoxLayout()
        countsLayout.addWidget(QLabel("Number of Digits:"))
        countsLayout.addWidget(self.numbersCountEdit)
        countsLayout.addWidget(QLabel("Number of Special Characters:"))
        countsLayout.addWidget(self.specialCharsCountEdit)

        # Add the counts layout to the main generator layout
        generatorLayout.addLayout(countsLayout)

        # Add other form components to the generator layout
        generatorLayout.addWidget(QLabel("Generated Password:"))
        generatorLayout.addWidget(self.generatedPasswordDisplay)

        lengthLayout = QHBoxLayout()
        lengthLayout.addWidget(QLabel("Password Length:"))
        lengthLayout.addWidget(self.lengthSlider)
        lengthLayout.addWidget(self.lengthSliderLabel)
        generatorLayout.addLayout(lengthLayout)

        # Add checkboxes to the generator layout
        generatorLayout.addWidget(self.includeUppercaseCheckbox)
        generatorLayout.addWidget(self.includeNumbersCheckbox)
        generatorLayout.addWidget(self.includeSpecialCharsCheckbox)

        # Add the generate button to the generator layout
        generatorLayout.addWidget(self.generateButton)
        
    def applyPasswordGeneratorSettings(self, pg_settings):
        """
        Applies saved settings to the password generator form components.
        
        :param pg_settings: A dictionary containing saved settings for the password generator.
        """
        # Apply settings to the length slider and label
        self.lengthSlider.setValue(pg_settings.get("length", 12))
        self.lengthSliderLabel.setText(str(pg_settings.get("length", 12)))

        # Apply settings to the inclusion checkboxes
        self.includeUppercaseCheckbox.setChecked(pg_settings.get("includeUppercase", True))
        self.includeNumbersCheckbox.setChecked(pg_settings.get("includeNumbers", True))
        self.includeSpecialCharsCheckbox.setChecked(pg_settings.get("includeSpecial", True))

        # Apply settings to the number of digits and special characters
        self.numbersCountEdit.setText(str(pg_settings.get("numDigits", 2)))
        self.specialCharsCountEdit.setText(str(pg_settings.get("numSpecial", 2)))

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
        """
        Clears all input fields in the add or edit password form. This method is typically
        called when preparing the form for a new entry or after saving an entry to reset the form.
        """
        self.website_name_entry.clear()
        self.website_url_entry.clear()
        self.username_entry.clear()
        self.password_entry.clear()
        self.notes_entry.clear()

    def populate_vault(self, entries=None, reselect_entry_id=None):
        """
        Populates the vault view with entries. If a specific subset of entries is provided, it displays those;
        otherwise, it fetches and displays entries based on the current mode (all, favourites, etc.).
        Additionally, it can reselect a previously selected entry based on an ID.

        Args:
            entries (list of tuples, optional): The specific entries to display. Defaults to None.
            reselect_entry_id (int, optional): The ID of an entry to reselect after repopulation. Defaults to None.
        """

        self.mainWindow.resetAutoLockTimer()  # Reset the auto-lock timer with user interaction.
        if self.selectedButton:
            # Deselect the previously selected entry if any.
            self.selectedButton.setSelected(False)
            self.selectedButton = None

        # Clear existing entries in the vault display.
        while self.scrollContentLayout.count():
            child = self.scrollContentLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Fetch entries based on the specified criteria or current mode.
        if entries is None:
            if self.currentMode == 'all':
                entries = self.db.fetch_all_entries(self.encryption_key)
            elif self.currentMode == 'favourites':
                entries = self.db.fetch_favourites(self.encryption_key)
            elif self.currentMode == 'alphabetical':
                entries = sorted(self.db.fetch_all_entries(self.encryption_key), key=lambda x: x[1].lower())
            elif self.currentMode == 'lastUpdated':
                entries = sorted(self.db.fetch_all_entries(self.encryption_key), key=lambda x: x[7], reverse=True)

        # Display each entry as a button in the vault view.
        for entry in entries:
            button = PasswordEntryButton(entry, self.themeManager)
            button.displayDetails.connect(lambda entry_data=entry, button=button: self.display_entry_details(entry_data, button))
            button.editClicked.connect(lambda entry_data=entry: self.enter_edit_mode(entry_data))
            button.deleteClicked.connect(lambda: self.delete_entry(entry[0]))
            button.toggleFavourite.connect(self.handle_toggle_favourite)
            self.scrollContentLayout.addWidget(button)

            # If a specific entry ID is meant to be reselected, do so.
            if reselect_entry_id is not None and entry[0] == reselect_entry_id:
                self.display_entry_details(entry, button)
                button.setSelected(True)
                self.selectedButton = button

    def search_vault(self):
        """
        Performs a search operation in the vault. Filters entries by the search query provided
        in the search input field and displays matching entries.

        This method also resets the auto-lock timer with each search operation.
        """
        self.mainWindow.resetAutoLockTimer()
        search_query = self.searchLineEdit.text().lower()
        # Assuming fetch_all_entries method exists and returns decrypted entries
        all_entries = self.db.fetch_all_entries(self.encryption_key)
        filtered_entries = [entry for entry in all_entries if search_query in entry[1].lower()]
        self.populate_vault(filtered_entries)

    def display_entry_details(self, entry_data, button):
        """
        Displays the details of a selected password entry in the UI's right column.

        Args:
            entry_data (tuple): Data of the selected entry.
            button (QPushButton): Reference to the button associated with this entry.
        """
        self.mainWindow.resetAutoLockTimer()  # Reset the auto-lock timer with user interaction.
        if self.selectedButton is not None:
            self.selectedButton.setSelected(False)  # Deselect the previously selected button.

        self.selectedButton = button  # Update reference to the newly selected button.
        self.selectedButton.setSelected(True)  # Highlight the selected button.

        # Display entry details in the right column fields.
        self.nameLineEdit.setText(entry_data[1])
        self.sitenameLineEdit.setText(entry_data[2] if len(entry_data) > 2 else "")
        self.usernameLineEdit.setText(entry_data[3] if len(entry_data) > 3 else "")
        self.passwordLineEdit.setText(entry_data[4] if len(entry_data) > 4 else "")
        self.notesTextEdit.setText(entry_data[5] if len(entry_data) > 5 else "")
        self.lastUpdatedLabel.setText(f"Last Updated: {entry_data[8]}" if len(entry_data) > 8 else "")

    def adjustButtonWidth(self):
        """
        Adjusts the width of buttons in the left column layout to maintain a consistent look
        and feel across different screen sizes.
        """
        for layout in [self.leftColumnLayout]:  # This can be extended to other layouts if needed.
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if isinstance(widget, QPushButton):
                    buttonWidth = int(self.width() * 0.2)  # Calculate button width as 20% of the widget's width.
                    widget.setFixedWidth(buttonWidth)

    def resizeEvent(self, event):
        """
        Handles the widget's resize event, adjusting the width of buttons accordingly.
        """
        self.mainWindow.resetAutoLockTimer()  # Reset the auto-lock timer with user interaction.
        self.adjustButtonWidth()  # Adjust button widths based on the new size.
        super().resizeEvent(event)  # Call the parent class's resize event handler.

    def delete_Entry(self, entry_id):
        """
        Deletes a password entry from the database and refreshes the vault view.

        Args:
            entry_id (int): The unique identifier of the entry to delete.
        """
        self.mainWindow.resetAutoLockTimer()  # Reset the auto-lock timer with user interaction.
        self.db.delete_password_entry(entry_id)  # Delete the entry from the database.

        # Refresh the vault view to reflect the changes.
        if self.searchLineEdit.text():
            self.search_vault()  # Refresh based on the current search term, if any.
        else:
            self.populate_vault()  # Refresh the entire vault view.

    def enter_edit_mode(self, entry_data):
        """
        Prepares the form for editing an existing password entry.

        Args:
            entry_data (tuple): Data of the entry to edit.
        """
        self.mainWindow.resetAutoLockTimer()  # Reset the auto-lock timer with user interaction.
        # Populate form fields with entry data for editing.
        self.website_name_entry.setText(entry_data[1])
        self.website_url_entry.setText(entry_data[2])
        self.username_entry.setText(entry_data[3])
        self.password_entry.setText(entry_data[4])
        self.notes_entry.setText(entry_data[5])
        self.current_edit_id = entry_data[0]  # Store the ID of the entry being edited.
        self.stackedWidget.setCurrentIndex(1)  # Switch to the add/edit form view.

    def handle_toggle_favourite(self, entry_id, _):
        """
        Toggles the favourite status of an entry.

        Args:
            entry_id (int): The ID of the entry for which to toggle the favourite status.
        """
        current_status = self.db.fetch_favourite_status(entry_id)  # Fetch the current status from the database.
        new_status = not current_status  # Calculate the new status.
        self.db.toggle_favourite_status(entry_id, new_status)  # Update the database with the new status.
        self.populate_vault(reselect_entry_id=entry_id)  # Refresh the UI to reflect the change.


    def changeMode(self, mode):
        """
        Changes the display mode of the vault to show all, favourites, in alphabetical order, or by last updated.

        Args:
            mode (str): The mode to change to ('all', 'favourites', 'alphabetical', 'lastUpdated').
        """
        self.mainWindow.resetAutoLockTimer()  # Reset the auto-lock timer with user interaction.
        self.currentMode = mode  # Update the current mode.
        self.populate_vault()  # Refresh the vault display based on the new mode.
        self.stackedWidget.setCurrentIndex(0)  # Ensure the vault view is displayed.

    def generate_password(self):
        """
        Generates a password based on user-specified criteria and displays it.
        """
        self.mainWindow.resetAutoLockTimer()  # Reset the auto-lock timer with user interaction.
        
        # Retrieve password criteria from UI components.
        length = self.lengthSlider.value()
        include_uppercase = self.includeUppercaseCheckbox.isChecked()
        num_digits = int(self.numbersCountEdit.text())
        num_special = int(self.specialCharsCountEdit.text())
        include_numbers = self.includeNumbersCheckbox.isChecked()
        include_special = self.includeSpecialCharsCheckbox.isChecked()

        # Compile settings based on user inputs.
        settings = {
            "length": length,
            "includeUppercase": include_uppercase,
            "numDigits": num_digits,
            "numSpecial": num_special,
            "includeNumbers": include_numbers,
            "includeSpecial": include_special
        }
        self.savePasswordGeneratorSettings(settings)  # Persist user-specified criteria.

        # Validate the criteria and generate the password.
        error_messages = self.validatePasswordCriteria(length, num_digits, num_special, include_numbers, include_special)
        if error_messages:
            self.displayPasswordOutput(error_messages[0], isError=True)  # Display the first encountered error message.
            return

        generated_password = PasswordGenerator.generate_password(length, include_uppercase, num_digits, num_special)
        self.displayPasswordOutput(generated_password, isError=False)  # Display the generated password.

    def saveSettingsOnChange(self):
        """
        Saves the password generator settings whenever any related UI component's state changes.
        """
        self.mainWindow.resetAutoLockTimer()  # Reset the auto-lock timer with user interaction.
        # Compile current settings from UI components.
        settings = {
            "length": self.lengthSlider.value(),
            "includeUppercase": self.includeUppercaseCheckbox.isChecked(),
            "numDigits": int(self.numbersCountEdit.text()) if self.numbersCountEdit.text().isdigit() else 0,
            "numSpecial": int(self.specialCharsCountEdit.text()) if self.specialCharsCountEdit.text().isdigit() else 0,
            "includeNumbers": self.includeNumbersCheckbox.isChecked(),
            "includeSpecial": self.includeSpecialCharsCheckbox.isChecked()
        }
        self.savePasswordGeneratorSettings(settings)  # Update saved settings.

    def savePasswordGeneratorSettings(self, settings):
        """
        Persists the password generator settings to a file.

        Args:
            settings (dict): The settings to save.
        """
        settings_path = get_settings_path()  # Retrieve the path to the settings file.
        try:
            with open(settings_path, 'r') as file:
                existing_settings = json.load(file)  # Load existing settings.
        except FileNotFoundError:
            existing_settings = {}  # Initialize settings if file not found.

        existing_settings["passwordGenerator"] = settings  # Update password generator settings.
        with open(settings_path, 'w') as file:
            json.dump(existing_settings, file, indent=4)  # Write updated settings back to file.

    def displayPasswordOutput(self, message, isError=False):
        """
        Displays a message in the password output display. Adjusts the styling for error messages.

        Args:
            message (str): The message to display.
            isError (bool): Flag indicating whether the message is an error message.
        """
        # Apply styling based on whether it's an error message.
        style = "color: red; font-weight: bold;" if isError else "color: black; font-weight: normal;"
        self.generatedPasswordDisplay.setStyleSheet(style)
        self.generatedPasswordDisplay.setText(message)  # Set the displayed message.

    def showOptionsDialog(self):
        """
        Opens the options dialog for adjusting application settings.
        """
        optionsDialog = OptionsDialog(self.themeManager, self)  # Initialize the dialog with the theme manager and current UI context.
        if optionsDialog.exec_() == QDialog.Accepted:
            self.applyGlobalSettings()  # Apply global settings if options are accepted.

    def applyPasswordVisibility(self):
        """
        Applies the global password visibility setting to all password fields.
        """
        show_passwords = self.settings.get('show_passwords', False)  # Retrieve the global setting for password visibility.
        self.passwordLineEdit.applyGlobalVisibilitySetting(show_passwords)  # Apply the setting to the password field.

    def applyGlobalSettings(self):
        """
        Reloads settings and applies them globally across the application UI.
        """
        self.settings = OptionsDialog.load_or_create_settings()  # Reload settings in case they were updated.
        self.applyPasswordVisibility()  # Apply password visibility settings.

    def showAddPasswordForm(self):
        """
        Switches the view to the add password form.
        """
        self.stackedWidget.setCurrentIndex(self.ADD_PASSWORD_FORM_INDEX)  # Set the current index to show the add password form.
        
    def showPasswordGeneratorForm(self):
        """
        Switches the view to the password generator form.
        """
        # Assuming PASSWORD_GENERATOR_FORM_INDEX is correctly defined
        print("Password Generator button clicked.") 
        self.stackedWidget.setCurrentIndex(self.PASSWORD_GENERATOR_FORM_INDEX)
        print(f"Switching to Password Generator form at index {self.PASSWORD_GENERATOR_FORM_INDEX}")
        print(f"Current stackedWidget index: {self.stackedWidget.currentIndex()}")
        print(f"Is stackedWidget visible? {self.stackedWidget.isVisible()}")
        print(f"Is form widget visible? {self.passwordGeneratorFormWidget.isVisible()}")
        
    def connectPasswordGeneratorSignals(self):
        """
        Connects signals from the UI components of the password generator form to their respective slots or methods.
        """
        self.generateButton.clicked.connect(self.generate_password_button_clicked)
        
    def generate_password_button_clicked(self):
        """
        Handles the "Generate Password" button click. Validates inputs, generates a password
        or displays an error message.
        """
        # Assume you've gathered all the necessary inputs from the form here
        # For demonstration, these variables are placeholders
        length = self.lengthSlider.value()
        include_uppercase = self.includeUppercaseCheckbox.isChecked()
        num_digits = int(self.numbersCountEdit.text())
        num_specials = int(self.specialCharsCountEdit.text())
        include_numbers = self.includeNumbersCheckbox.isChecked()
        include_specials = self.includeSpecialCharsCheckbox.isChecked()
        
        # Error handling
        if (not include_numbers and num_digits > 0) or (not include_specials and num_specials > 0) or (num_digits + num_specials > length):
            error_message = "Error: Check your settings. Criteria do not match the length or checkboxes."
            self.displayPasswordOutput(error_message, isError=True)
            return
        
        # Generate the password
        generated_password = PasswordGenerator.generate_password(length, include_uppercase, num_digits, num_specials)
        self.displayPasswordOutput(generated_password, isError=False)

    def displayPasswordOutput(self, message, isError=False):
        """
        Displays a message in the generatedPasswordDisplay QLineEdit and adjusts the text color
        based on the current theme and whether it's an error message.
        """
        # Determine text color based on the current theme and whether it's an error
        currentTheme = self.themeManager.currentTheme()
        if currentTheme == "dark":
            textColor = "white" if not isError else "red"
        else:
            textColor = "black" if not isError else "red"

        # Apply the determined text color
        self.generatedPasswordDisplay.setStyleSheet(f"color: {textColor};")
        self.generatedPasswordDisplay.setText(message)