from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QCursor
import os

class PasswordEntryButton(QWidget):
    """
    Custom widget representing a password entry in the vault, providing options to display details, edit, delete, or toggle favourite status.

    Attributes:
        displayDetails (pyqtSignal): Signal emitted when the button is clicked to display entry details.
        editClicked (pyqtSignal): Signal emitted when the edit icon is clicked.
        deleteClicked (pyqtSignal): Signal emitted when the delete icon is clicked.
        toggleFavourite (pyqtSignal): Signal emitted to toggle the favourite status of the entry.
    """
    displayDetails = pyqtSignal(object, object)
    editClicked = pyqtSignal(object)
    deleteClicked = pyqtSignal(object)
    toggleFavourite = pyqtSignal(int, bool)

    def __init__(self, entry_data, themeManager, *args, **kwargs):
        """
        Initialize a PasswordEntryButton widget.

        Args:
            entry_data (tuple): Data of the password entry containing details such as website name, URL, username, password, notes, favourite status, and timestamps.
            themeManager (ThemeManager): Reference to the application's theme manager to handle theme-related changes.
            *args: Variable length argument list passed to the QWidget initializer.
            **kwargs: Arbitrary keyword arguments passed to the QWidget initializer.

        Initializes the layout, button, and icons for the password entry. Connects signals for theme changes and icon clicks to corresponding slots/methods.
        """
        super(PasswordEntryButton, self).__init__(*args, **kwargs)
        self.entry_data = entry_data  # Data of the password entry.
        self.themeManager = themeManager  # Reference to the application's theme manager.

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(10)

        self.button = QPushButton(entry_data[1])  # Display website name on the button.
        self.button.clicked.connect(self.onDisplayDetails)
        self.button.setCheckable(True)
        self.button.setFocusPolicy(Qt.NoFocus)

        # Setup icons for editing, deleting, and toggling favourite status.
        self.setupIcons()

        # Connect the themeChanged signal from the ThemeManager to the updateIcons slot.
        self.themeManager.themeChanged.connect(self.updateIcons)
        
        # Initial call to set icons according to the current theme.
        self.updateIcons(self.themeManager.currentTheme())

        # Add components to the layout.
        self.layout.addWidget(self.button, 1)
        self.layout.addWidget(self.editIcon)
        self.layout.addWidget(self.deleteIcon)
        self.layout.addWidget(self.favouriteIcon)

        # Setup icon click event handlers.
        self.setupIconClickHandlers()
           
    def onDisplayDetails(self):
        """
        Handler for the main button click event to emit displayDetails signal with entry data.
        """
        self.displayDetails.emit(self.entry_data, self)

    def setupIcons(self):
        """
        Initializes icons and hides them by default.
        """
        self.editIcon = QLabel(self)
        self.editIcon.hide()
        self.editIcon.setCursor(QCursor(Qt.PointingHandCursor))
        self.editIcon.setToolTip("Edit")
        
        self.deleteIcon = QLabel(self)
        self.deleteIcon.hide()
        self.deleteIcon.setCursor(QCursor(Qt.PointingHandCursor))
        self.deleteIcon.setToolTip("Delete")
        
        self.favouriteIcon = QLabel(self)
        self.favouriteIcon.hide()  # Initially hidden
        self.favouriteIcon.setCursor(QCursor(Qt.PointingHandCursor))
        self.favouriteIcon.setToolTip("Toggle Favourite")

    def setupIconClickHandlers(self):
        """
        Assigns click event handlers to the icons.
        """
        self.editIcon.mousePressEvent = lambda event: self.editClicked.emit(self.entry_data)
        self.deleteIcon.mousePressEvent = lambda event: self.deleteClicked.emit(self.entry_data)
        self.favouriteIcon.mousePressEvent = lambda event: self.onFavouriteClicked(event)
        
    def onFavouriteClicked(self, event):
        """
        Handler for the favourite icon click event to toggle the favourite status.
        """
        current_status_bool = self.entry_data[6] == 1
        self.toggleFavourite.emit(self.entry_data[0], not current_status_bool)

    def setSelected(self, isSelected):
        """
        Updates the visibility of icons based on selection state and applies custom styling.

        Args:pass
            isSelected (bool): Indicates if the entry is selected.
        """
        self.editIcon.setVisible(isSelected)
        self.deleteIcon.setVisible(isSelected)
        self.favouriteIcon.setVisible(isSelected)
        
        self.button.setProperty('isSelected', isSelected)
        self.button.style().unpolish(self.button)
        self.button.style().polish(self.button)

        
    def updateIcons(self, themeName):
        """
        Updates the icons for edit, delete, and favourite actions according to the current theme.

        This method dynamically changes the icons based on the theme, ensuring that they are
        visible against the theme's background. It scales the icons to fit the button's size and
        applies them to the respective labels.

        Args:
            themeName (str): The name of the current theme ('light' or 'dark') which determines the icon set to use.
        """
        # Determine the base path for resources relative to this file's location.
        basePath = os.path.dirname(os.path.abspath(__file__))
        resourcesPath = os.path.abspath(os.path.join(basePath, '..', '..', 'resources', 'icons'))

        # Define the scale factor and calculate the icon size.
        scaleFactor = 0.5
        iconSize = QSize(int(self.button.sizeHint().height() * scaleFactor),
                        int(self.button.sizeHint().height() * scaleFactor))

        # Helper function to load an icon with logging for debugging.
        def loadIcon(iconName):
            iconPath = os.path.join(resourcesPath, iconName)
            pixmap = QPixmap(iconPath).scaled(iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if pixmap.isNull():
                print(f"Failed to load icon: {iconPath}")
            return pixmap

        # Update the edit icon.
        editIconName = 'edit.png' if themeName == 'light' else 'edit_white.png'
        self.editIcon.setPixmap(loadIcon(editIconName))

        # Update the delete icon.
        deleteIconName = 'delete.png' if themeName == 'light' else 'delete_white.png'
        self.deleteIcon.setPixmap(loadIcon(deleteIconName))

        # Update the favourite icon based on the favourite status and theme.
        favIconFile = 'heart_favourited.png' if self.entry_data[6] == 1 else 'heart_empty.png'
        favIconFileWhite = 'heart_favourited.png' if self.entry_data[6] == 1 else 'heart_empty_white.png'
        favIconName = favIconFile if themeName == 'light' else favIconFileWhite
        self.favouriteIcon.setPixmap(loadIcon(favIconName))
