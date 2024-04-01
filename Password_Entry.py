from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QCursor

class PasswordEntryButton(QWidget):
    displayDetails = pyqtSignal(object, object)
    editClicked = pyqtSignal(object)
    deleteClicked = pyqtSignal(object)
    toggleFavourite = pyqtSignal(int, bool)

    def __init__(self, entry_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry_data = entry_data

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(10)

        self.button = QPushButton(entry_data[1])
        self.button.clicked.connect(self.onDisplayDetails)
        self.button.setCheckable(True)
        self.button.setFocusPolicy(Qt.NoFocus)

        scaleFactor = 0.5
        iconSize = QSize(int(self.button.sizeHint().height() * scaleFactor),
                        int(self.button.sizeHint().height() * scaleFactor))

        # Edit Icon setup
        self.editIcon = QLabel(self)
        editPixmap = QPixmap('Icons/edit.png').scaled(iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.editIcon.mousePressEvent = self.onEditClicked
        self.editIcon.setPixmap(editPixmap)
        self.editIcon.hide()
        self.editIcon.setCursor(QCursor(Qt.PointingHandCursor))
        self.editIcon.setToolTip("Edit")
        
        # Delete Icon setup
        self.deleteIcon = QLabel(self)
        deletePixmap = QPixmap('Icons/delete.png').scaled(iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.deleteIcon.mousePressEvent = self.onDeleteClicked
        self.deleteIcon.setPixmap(deletePixmap)
        self.deleteIcon.hide()
        self.deleteIcon.setCursor(QCursor(Qt.PointingHandCursor))
        self.deleteIcon.setToolTip("Delete")

        # Favourite Icon setup
        self.favouriteIcon = QLabel(self)  # Make sure this line is correctly included
        self.favouriteIcon.mousePressEvent = self.onFavouriteClicked
        self.favouriteIcon.setVisible(False)
        isFavourite = entry_data[6] == 1
        print(isFavourite)
        self.entryID = entry_data[0]
        favIconPath = 'Icons/heart_favourited.png' if isFavourite else 'Icons/heart_empty.png'
        favIconPixmap = QPixmap(favIconPath).scaled(iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.favouriteIcon.setPixmap(favIconPixmap)
        self.favouriteIcon.setCursor(QCursor(Qt.PointingHandCursor))
        self.favouriteIcon.setToolTip("Toggle Favourite")
        self.favouriteIcon.mousePressEvent = lambda event: self.toggleFavourite.emit(self.entry_data[0], self.entry_data[6] == 1)
 

        # Adding widgets to the layout
        self.layout.addWidget(self.button, 1)
        self.layout.addWidget(self.editIcon)
        self.layout.addWidget(self.deleteIcon)
        self.layout.addWidget(self.favouriteIcon)  # Ensure this is correctly added after initialization

        self.applyStylesheet()

    def applyStylesheet(self):
        self.setStyleSheet("""
            PasswordEntryButton {
                /* Add styles for the overall widget here if needed */
            }
            QPushButton {
                border: 1px solid #a9a9a9;
                border-radius: 20px;
                padding: 10px;
                color: black;
                text-align: left;
                padding-left: 20px;
                background-color: #ffffff; /* Default background color is white */
            }
            QPushButton:hover {
                background-color: #e0e0e0; /* Grey color when hovered */
            }
            QPushButton:checked {
                background-color: #F5C754; /* Yellow color for the selected button */
            }
            QLabel {
                /* Icons */
            }
        """)
        
    def updateStyle(self, isSelected):
        if isSelected:
            # Apply styles for selected state
            self.button.setStyleSheet("""
                QPushButton {
                    border: 1px solid #a9a9a9;
                    border-radius: 20px;
                    padding: 10px;
                    color: black;
                    text-align: left;
                    padding-left: 20px;
                    background-color: #F5C754; /* Yellow color for the selected button */
                }
            """)
        else:
            # Apply default styles for unselected state
            self.button.setStyleSheet("""
                QPushButton {
                    border: 1px solid #a9a9a9;
                    border-radius: 20px;
                    padding: 10px;
                    color: black;
                    text-align: left;
                    padding-left: 20px;
                    background-color: #ffffff; /* Default background color is white */
                }
                QPushButton:hover {
                    background-color: #e0e0e0; /* Grey color when hovered */
                }
            """)
            
    def onDisplayDetails(self):
        self.displayDetails.emit(self.entry_data, self)

    def onEditClicked(self, event):
        print("Edit clicked for entry ID:", self.entry_data[0])
        self.editClicked.emit(self.entry_data)

    def onDeleteClicked(self, event):
        print("Delete clicked for entry ID:", self.entry_data[0])
        self.deleteClicked.emit(self.entry_data)
        
    def onFavouriteClicked(self, event):
        # Emit the toggleFavourite signal with correct parameters
        current_status = self.entry_data[6] == 1
        self.toggleFavourite.emit(self.entry_data[0], current_status)
        

    def setSelected(self, isSelected):
        # Show or hide the edit and delete icons based on the isSelected flag
        self.editIcon.setVisible(isSelected)
        self.deleteIcon.setVisible(isSelected)
        
        # Additionally, control the visibility of the favourite icon the same way
        self.favouriteIcon.setVisible(isSelected)

        # Update the style of the button to reflect its selection state
        self.updateStyle(isSelected)