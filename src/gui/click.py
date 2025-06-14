from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QFrame, QButtonGroup, QCheckBox)

class ClickTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup for the click tab with regular options frame"""
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 8)  # Reduced bottom margin
        layout.setSpacing(12)
        
        # Button section (Random/Record)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        # Button group for exclusivity
        button_group = QButtonGroup(self)
        
        random_btn = QPushButton("Random")
        random_btn.setObjectName("optionButton")
        random_btn.setCheckable(True)
        random_btn.setChecked(True)
        
        record_btn = QPushButton("Record")
        record_btn.setObjectName("optionButton")
        record_btn.setCheckable(True)
        
        # Add buttons to the group
        button_group.addButton(random_btn)
        button_group.addButton(record_btn)
        button_group.setExclusive(True)
        
        # Make buttons fill all available width
        button_layout.addWidget(random_btn, 1)
        button_layout.addWidget(record_btn, 1)
        
        # Options frame with background
        options_frame = QFrame()
        options_frame.setObjectName("optionsFrameWithBg")
        options_layout = QVBoxLayout(options_frame)
        options_layout.setContentsMargins(12, 12, 12, 12)
        options_layout.setSpacing(8)
        
        # Add 2 options as checkboxes (original style)
        option1 = QCheckBox("Option 1")
        option2 = QCheckBox("Option 2")
        
        options_layout.addWidget(option1)
        options_layout.addWidget(option2)
        
        # Add all elements to the tab's main layout
        layout.addLayout(button_layout)
        layout.addWidget(options_frame)
        # Removed speed section from this tab
        
        self.setLayout(layout)