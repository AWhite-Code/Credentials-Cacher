from PyQt5.QtWidgets import QApplication
from Window import MainWindow

def main():
    app = QApplication([])  # Create an instance of QApplication
    main_window = MainWindow()  # Now you can create your MainWindow
    main_window.show()  # Show the main window
    app.exec_()  # Start the application's event loop

if __name__ == "__main__":
    main()