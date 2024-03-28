from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QVBoxLayout

class VaultWidget(QWidget):
    def __init__(self, parent=None):
        super(VaultWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        title_label = QLabel("Password Vault", self)
        layout.addWidget(title_label, 0, 0, 1, 3)
        
        self.add_password_button = QPushButton("Add Password", self)
        layout.addWidget(self.add_password_button, 1, 0)
        
        self.add_password_container = QWidget(self)
        add_password_layout = QVBoxLayout(self.add_password_container)
        
        self.website_name_entry = QLineEdit(self.add_password_container)
        self.website_name_entry.setPlaceholderText("Website Name")
        self.website_url_entry = QLineEdit(self.add_password_container)
        self.website_url_entry.setPlaceholderText("Website URL")
        self.username_entry = QLineEdit(self.add_password_container)
        self.username_entry.setPlaceholderText("Username")
        self.password_entry = QLineEdit(self.add_password_container)
        self.password_entry.setPlaceholderText("Password")
        self.notes_entry = QLineEdit(self.add_password_container)
        self.notes_entry.setPlaceholderText("Notes")

        # Add all widgets to the layout
        add_password_layout.addWidget(self.website_name_entry)
        add_password_layout.addWidget(self.website_url_entry)
        add_password_layout.addWidget(self.username_entry)
        add_password_layout.addWidget(self.password_entry)
        add_password_layout.addWidget(self.notes_entry)
        
        self.password_entry.setEchoMode(QLineEdit.Password)
        
        self.submit_button = QPushButton("Submit", self.add_password_container)
        add_password_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.submit_password_details)

        layout.addWidget(self.add_password_container, 2, 0, 1, 3)
        self.add_password_container.hide()  # Initially hidden

        self.setStyleSheet("""
            QWidget {
                font: 15px;
            }
            QLineEdit {
                border: 2px solid #a9a9a9;
                border-radius: 15px;
                padding: 5px;
                background-color: white;
                color: black;
            }
            QLineEdit:hover {
                border: 2px solid #f0f0f0;
            }
            QPushButton {
                border: 2px solid #a9a9a9;
                border-radius: 15px;
                padding: 5px;
                background-color: #0078d7;
                color: white;
            }
            QPushButton:hover {
                background-color: #0053a6;
            }
            QPushButton:pressed {
                background-color: #00397a;
            }
        """)
        
        self.add_password_button.clicked.connect(self.toggle_add_password_container)

    def toggle_add_password_container(self):
        # Toggle the visibility of the add_password_container
        self.add_password_container.setVisible(not self.add_password_container.isVisible())
        
    def submit_password_details(self):
        website_name = self.website_name_entry.text()
        website_url = self.website_url_entry.text()
        username = self.username_entry.text()
        password = self.password_entry.text()
        notes = self.notes_entry.text()
        
        # Here you'd call your database insertion method, passing the collected data
        # For now, let's just print the data to confirm the method is being called
        print("Submitting:", website_name, website_url, username, password, notes)