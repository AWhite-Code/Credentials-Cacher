from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
import re
import pickle
from core.Hashing import Hashing
import os

class RegistrationWidget(QWidget):
    """
    A widget that facilitates user registration. It prompts the user to input a username and password, 
    ensures the password meets specified criteria, and provides feedback on the registration process.

    Attributes:
        db (Database): An instance of the application's database connection, used to interact with the database.
        main_window (MainWindow): The main application window instance, facilitating navigation between views.
        username_entry (QLineEdit, optional): Input field for the username. Initialized to None.
        password_entry (QLineEdit, optional): Input field for the password. Initialized to None.
        confirm_password_entry (QLineEdit, optional): Input field for confirming the password. Initialized to None.
    """
    
    def __init__(self, db, main_window, parent=None):
        """
        Initializes a new instance of the RegistrationWidget.

        Args:
            db (Database): The application's database connection object.
            main_window (MainWindow): The main window of the application.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.main_window = main_window
        self.db = db
        # Initialize form fields to None or appropriate default values
        self.username_entry = None
        self.password_entry = None
        self.confirm_password_entry = None
        self.init_ui()

    def init_ui(self):
        """
        Sets up the UI components for the registration widget.

        This method organizes the registration form into a two-column layout. 
        The left column displays a logo and password requirements, while the right column contains
        the form fields for username, password, and password confirmation, along with submission buttons.
        """
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        grid_layout = QHBoxLayout()
        left_column_layout = self.initialize_left_column()
        right_column_layout = self.initialize_right_column()

        grid_layout.addLayout(left_column_layout, 2)  # Left column has a larger ratio
        grid_layout.addLayout(right_column_layout, 1)  # Right column contains the form fields
        self.layout().addLayout(grid_layout)

    def initialize_left_column(self):
        """Sets up the left column with the application logo and password requirements."""
        left_column_layout = QVBoxLayout()
        left_column_layout.setAlignment(Qt.AlignTop)
        left_column_layout.addLayout(self.setup_logo())
        left_column_layout.addWidget(QWidget(), 20)  # Spacer
        left_column_layout.addWidget(self.create_password_requirements_label())
        return left_column_layout

    def setup_logo(self):
        """Prepares the logo component based on the current theme setting."""
        logo_layout = QHBoxLayout()
        logo_spacer = QWidget()
        logo_spacer.setFixedWidth(20)
        logo_layout.addWidget(logo_spacer)

        # Determine and set the appropriate logo based on the theme.
        dark_mode_enabled = self.main_window.settings.get('dark_mode', False)
        logo_filename = "logo_white.svg" if dark_mode_enabled else "logo.svg"
        logo_path = os.path.join('resources', 'icons', logo_filename)
        self.logoContainer = QSvgWidget(logo_path, self)
        logo_layout.addWidget(self.logoContainer)

        return logo_layout

    def initialize_right_column(self):
        """Sets up the right column with form fields and action buttons."""
        right_column_layout = QVBoxLayout()
        right_column_layout.setAlignment(Qt.AlignTop)
        self.setup_form_fields(right_column_layout)

        if os.path.exists(os.path.join(os.getenv('APPDATA'), 'Credentials Cacher', 'credentials.bin')):
            self.setup_return_to_login_button(right_column_layout)
        self.setup_register_button(right_column_layout)

        return right_column_layout

    def create_password_requirements_label(self):
        """Generates a label detailing the password creation requirements."""
        requirements_html = """
        <p><strong>Password Requirements:</strong></p>
        <ul>
            <li>At least 20 characters long</li>
            <li>At least one number</li>
            <li>At least one special character</li>
            <li>A mix of uppercase and lowercase letters</li>
        </ul>
        """
        label = QLabel(requirements_html, self)
        label.setTextFormat(Qt.RichText)
        return label

    def setup_form_fields(self, layout):
        """Creates and adds username and password fields to the given layout."""
        self.username_entry = self.create_form_field("Username", "Enter your username")
        layout.addWidget(self.username_entry)

        layout.addWidget(QWidget(), 20)  # Spacer

        self.password_entry = self.create_form_field("Password", "Enter your password", is_password=True)
        layout.addWidget(self.password_entry)

        layout.addWidget(QWidget(), 20)  # Spacer

        self.confirm_password_entry = self.create_form_field("Confirm Password", "Confirm your password", is_password=True)
        layout.addWidget(self.confirm_password_entry)

    def create_form_field(self, label_text, placeholder, is_password=False):
        """Creates a form field with a label and input field."""
        label = QLabel(label_text)
        field = QLineEdit(self)
        field.setPlaceholderText(placeholder)
        if is_password:
            field.setEchoMode(QLineEdit.Password)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(field)
        return field

    def setup_return_to_login_button(self, layout):
        """Adds a button to return to the login screen."""
        button = QPushButton("Return to Login", self)
        button.clicked.connect(self.main_window.show_login)
        layout.addWidget(button)

    def setup_register_button(self, layout):
        """Adds a registration submission button."""
        button = QPushButton("Register", self)
        button.clicked.connect(self.register_action)
        layout.addWidget(button)


    def register_action(self):
        """
        Validates user inputs and registers the user if the criteria are met, displaying appropriate success or failure messages.
        Enhanced error handling includes checks for empty input fields.
        """
        # Strip whitespace from username and retrieve passwords
        username = self.username_entry.text().strip()
        password = self.password_entry.text()
        confirm_password = self.confirm_password_entry.text()

        # Check for empty username field
        if not username:
            QMessageBox.warning(self, "Registration Failed", "Username cannot be empty.")
            return

        # Check for empty password fields
        if not password or not confirm_password:
            QMessageBox.warning(self, "Registration Failed", "Password fields cannot be empty.")
            return

        # Password match check
        if password != confirm_password:
            QMessageBox.warning(self, "Registration Failed", "The passwords do not match.")
            return

        # Password requirements validation
        if not self.validate_password(password):
            QMessageBox.warning(self, "Registration Failed", "The password does not meet the requirements.")
            return

        # Attempt to save credentials and notify the user
        try:
            hashed_password = Hashing.hash_password(password)
            self.save_credentials(username, hashed_password)
            QMessageBox.information(self, "Registration Successful", "You have been successfully registered.")
            self.db.wipe_database()  # Cleanup database as needed
            self.main_window.show_login()  # Navigate back to the login screen
        except Exception as e:
            QMessageBox.warning(self, "Registration Error", "An error occurred during registration. Please try again.")
            print(f"Registration error: {e}")  # Logging the error can help with debugging


    def clear_credentials(self):
        open('credentials.bin', 'wb').close()

    def validate_password(self, password):
        """Validates the password against the set requirements."""
        if len(password) < 8 or not re.search("[0-9]", password) or not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True
    
    def save_credentials(self, username, hashed_password):
        """
        Saves the registered user's credentials securely to a binary file.

        Args:
            username (str): The registered username.
            hashed_password (str): The hashed password for the user.
        """
        app_data_path = os.getenv('APPDATA')
        app_directory = os.path.join(app_data_path, 'Credentials Cacher')

        if not os.path.exists(app_directory):
            os.makedirs(app_directory)

        credentials_path = os.path.join(app_directory, 'credentials.bin')
        credentials = {'username': username, 'password': hashed_password}
        with open(credentials_path, 'wb') as file:
            pickle.dump(credentials, file)

    def resizeEvent(self, event):
        """
        Handles resize events for the widget, adjusting the logo and form field sizes dynamically.

        Args:
            event: The event object containing details about the resize event.
        """
        super().resizeEvent(event)
        logo_width = int(self.size().width() * 0.4)
        logo_height = int(self.size().height() * 0.55)
        self.logoContainer.setFixedSize(logo_width, logo_height)

        if self.username_entry and self.password_entry and self.confirm_password_entry:
            field_width = max(200, int(self.size().width() * 0.3))
            for field in [self.username_entry, self.password_entry, self.confirm_password_entry]:
                field.setMaximumWidth(field_width)