from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QCursor

class PasswordEntryButton(QWidget):
    displayDetails = pyqtSignal(object, object)
    editClicked = pyqtSignal(object)
    deleteClicked = pyqtSignal(object)

    def __init__(self, entry_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry_data = entry_data

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(10)

        self.button = QPushButton(entry_data[1])  # Assuming entry_data[1] is the label text
        self.button.clicked.connect(self.onDisplayDetails)
        self.button.setCheckable(True)
        self.button.setFocusPolicy(Qt.NoFocus)

        # Scale factor to determine icon size as a fraction of button height
        scaleFactor = 0.5

        # Calculate icon size based on button height and scale factor
        iconSize = QSize(int(self.button.sizeHint().height() * scaleFactor),
                        int(self.button.sizeHint().height() * scaleFactor))

        self.editIcon = QLabel(self)
        editPixmap = QPixmap('Icons/edit.png').scaled(iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.editIcon.setPixmap(editPixmap)
        self.editIcon.hide()
        self.editIcon.setCursor(QCursor(Qt.PointingHandCursor))
        self.editIcon.setToolTip("Edit")  # Set tooltip for edit icon

        self.deleteIcon = QLabel(self)
        deletePixmap = QPixmap('Icons/delete.png').scaled(iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.deleteIcon.setPixmap(deletePixmap)
        self.deleteIcon.hide()
        self.deleteIcon.setCursor(QCursor(Qt.PointingHandCursor))
        self.deleteIcon.setToolTip("Delete")  # Set tooltip for delete icon

        self.layout.addWidget(self.button, 1)
        self.layout.addWidget(self.editIcon)
        self.layout.addWidget(self.deleteIcon)

        self.editIcon.mousePressEvent = self.onEditClicked
        self.deleteIcon.mousePressEvent = self.onDeleteClicked

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
        self.editClicked.emit(self.entry_data)

    def onDeleteClicked(self, event):
        self.deleteClicked.emit(self.entry_data)
        

    def setSelected(self, isSelected):
        self.editIcon.setVisible(isSelected)
        self.deleteIcon.setVisible(isSelected)
        self.updateStyle(isSelected)