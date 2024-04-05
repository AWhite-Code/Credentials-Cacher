from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QCursor

class PasswordEntryButton(QWidget):
    displayDetails = pyqtSignal(object, object)
    editClicked = pyqtSignal(object)
    deleteClicked = pyqtSignal(object)
    toggleFavourite = pyqtSignal(int, bool)

    def __init__(self, entry_data, themeManager, *args, **kwargs):
        super(PasswordEntryButton, self).__init__(*args, **kwargs)
        self.entry_data = entry_data
        self.themeManager = themeManager

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(10)

        self.button = QPushButton(entry_data[1])
        self.button.clicked.connect(self.onDisplayDetails)
        self.button.setCheckable(True)
        self.button.setFocusPolicy(Qt.NoFocus)

        # Initialize editIcon, deleteIcon, and favouriteIcon before calling updateIcons
        scaleFactor = 0.5
        iconSize = QSize(int(self.button.sizeHint().height() * scaleFactor),
                         int(self.button.sizeHint().height() * scaleFactor))
        
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

        # Connect the themeChanged signal from the ThemeManager to the updateIcons slot
        self.themeManager.themeChanged.connect(self.updateIcons)
        
        # Now it's safe to call updateIcons
        self.updateIcons(self.themeManager.currentTheme())

        self.layout.addWidget(self.button, 1)
        self.layout.addWidget(self.editIcon)
        self.layout.addWidget(self.deleteIcon)
        self.layout.addWidget(self.favouriteIcon)

        # Setup mousePressEvent for icons
        self.editIcon.mousePressEvent = lambda event: self.editClicked.emit(self.entry_data)
        self.deleteIcon.mousePressEvent = lambda event: self.deleteClicked.emit(self.entry_data)
        self.favouriteIcon.mousePressEvent = lambda event, id=self.entry_data[0], fav=self.entry_data[6] == 1: self.toggleFavourite.emit(id, fav)
           
    def onDisplayDetails(self):
        self.displayDetails.emit(self.entry_data, self)

    def onEditClicked(self, event):
        print("Edit clicked for entry ID:", self.entry_data[0])
        self.editClicked.emit(self.entry_data)

    def onDeleteClicked(self, event):
        print("Delete clicked for entry ID:", self.entry_data[0])
        self.deleteClicked.emit(self.entry_data)
        
    def onFavouriteClicked(self, event):
        # Correctly interpret the current status as a boolean
        current_status_bool = self.entry_data[6] == 1
        print(f"Favourite clicked for entry ID: {self.entryID}, current status: {current_status_bool}")
        # Emit the signal with the current boolean status
        self.toggleFavourite.emit(self.entryID, current_status_bool)
        

    def setSelected(self, isSelected):
        self.editIcon.setVisible(isSelected)
        self.deleteIcon.setVisible(isSelected)
        self.favouriteIcon.setVisible(isSelected)
        
        # Set a custom property that can be used in the stylesheet
        self.button.setProperty('isSelected', isSelected)
        self.button.style().unpolish(self.button)
        self.button.style().polish(self.button)
        
    def updateIcons(self, themeName):
        scaleFactor = 0.5
        iconSize = QSize(int(self.button.sizeHint().height() * scaleFactor),
                         int(self.button.sizeHint().height() * scaleFactor))
        
        # Update edit icon
        editIconPath = 'Icons/edit.png' if themeName == 'light' else 'Icons/edit_white.png'
        editPixmap = QPixmap(editIconPath).scaled(iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.editIcon.setPixmap(editPixmap)
        
        # Update delete icon
        deleteIconPath = 'Icons/delete.png' if themeName == 'light' else 'Icons/delete_white.png'
        deletePixmap = QPixmap(deleteIconPath).scaled(iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.deleteIcon.setPixmap(deletePixmap)
        
        # Update favourite icon if necessary
        isFavourite = self.entry_data[6] == 1
        favIconPath = 'Icons/heart_favourited.png' if isFavourite else 'Icons/heart_empty.png'
        if themeName == 'dark':
            favIconPath = 'Icons/heart_favourited' if isFavourite else 'Icons/heart_empty_white.png'
        favIconPixmap = QPixmap(favIconPath).scaled(iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.favouriteIcon.setPixmap(favIconPixmap)