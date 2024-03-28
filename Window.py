from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QStackedWidget
from PyQt5.QtCore import QSize, Qt
from Login import LoginWidget
from Vault_Window import VaultWidget
from Registration import RegistrationWidget
import os
import pickle

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Credentials Cacher")
        
        # Set initial size to 40% of the screen's width and height
        screen_size = QApplication.primaryScreen().size()
        width = int(screen_size.width() * 0.4)  # Ensure width is an integer
        height = int(screen_size.height() * 0.4)  # Ensure height is an integer
        self.resize(width, height)  # This should now work without type errors

        # Initialize stack for widgets
        self.stacked_widgets = QStackedWidget()
        self.setCentralWidget(self.stacked_widgets)

        # Initialize widgets
        self.login_widget = LoginWidget(self.toggle_widgets, self)
        self.registration_widget = RegistrationWidget(self.toggle_widgets)
        self.vault_widget = VaultWidget()

        # Add widgets to the stack
        self.stacked_widgets.addWidget(self.registration_widget)
        self.stacked_widgets.addWidget(self.login_widget)
        self.stacked_widgets.addWidget(self.vault_widget)

        # Decide which widget to show on start
        self.current_widget = self.login_widget if self.check_credentials_exist() else self.registration_widget
        self.stacked_widgets.setCurrentWidget(self.current_widget)

    def toggle_widgets(self):
        if self.stacked_widgets.currentWidget() == self.login_widget:
            self.stacked_widgets.setCurrentWidget(self.registration_widget)
        else:
            self.stacked_widgets.setCurrentWidget(self.login_widget)

    def check_credentials_exist(self):
        # Check if the binary file exists and is not empty
        if os.path.exists('credentials.bin'):
            try:
                with open('credentials.bin', 'rb') as file: # Try to load the credentials
                    credentials = pickle.load(file)
                    return bool(credentials)                # Return True if credentials are not empty
            except EOFError:                                # Empty file
                return False
        return False

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()