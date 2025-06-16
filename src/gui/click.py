from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QButtonGroup, QFrame,
                             QSpinBox, QCheckBox)
from PyQt6.QtCore import Qt
from src.functions.click import update_click_type, update_position, update_jitter, update_delay, update_limit

class ClickTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup for the click tab with compact buttons"""
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 8)
        layout.setSpacing(10)
        
        # -- Click Type Section with small buttons --
        type_section = QVBoxLayout()
        type_section.setSpacing(4)
        type_label = QLabel("Click Type")
        type_label.setObjectName("sectionLabel")
        type_section.addWidget(type_label)
        
        # Button grid for click types (2x2)
        type_grid = QHBoxLayout()
        type_grid.setSpacing(6)
        
        # Create button group
        self.type_group = QButtonGroup(self)
        self.type_group.setExclusive(True)
        
        # Create small buttons
        left_btn = QPushButton("Left")
        right_btn = QPushButton("Right")
        double_btn = QPushButton("Double")
        middle_btn = QPushButton("Middle")
        
        # Set compact style
        for btn in [left_btn, right_btn, double_btn, middle_btn]:
            btn.setObjectName("compactButton")
            btn.setCheckable(True)
            btn.setFixedHeight(28)  # Reduced height
        
        # Default selection
        left_btn.setChecked(True)
        
        # Add buttons to group with IDs
        self.type_group.addButton(left_btn, 1)
        self.type_group.addButton(right_btn, 2)
        self.type_group.addButton(double_btn, 3)
        self.type_group.addButton(middle_btn, 4)
        
        # Connect group to function
        self.type_group.buttonClicked.connect(self.update_click_type)
        
        # Add buttons to grid
        type_grid.addWidget(left_btn, 1)
        type_grid.addWidget(right_btn, 1)
        type_grid.addWidget(double_btn, 1)
        type_grid.addWidget(middle_btn, 1)
        
        type_section.addLayout(type_grid)
        
        # -- Position Section --
        position_section = QVBoxLayout()
        position_section.setSpacing(4)
        position_label = QLabel("Click Position")
        position_label.setObjectName("sectionLabel")
        position_section.addWidget(position_label)
        
        position_row = QHBoxLayout()
        position_row.setSpacing(6)
        
        # Create button group
        self.position_group = QButtonGroup(self)
        self.position_group.setExclusive(True)
        
        # Create small buttons
        current_btn = QPushButton("Current")
        random_btn = QPushButton("Random")
        
        # Set compact style
        for btn in [current_btn, random_btn]:
            btn.setObjectName("compactButton")
            btn.setCheckable(True)
            btn.setFixedHeight(28)  # Reduced height
        
        # Default selection
        current_btn.setChecked(True)
        
        # Add to group
        self.position_group.addButton(current_btn, 1)
        self.position_group.addButton(random_btn, 2)
        
        # Connect
        self.position_group.buttonClicked.connect(self.update_position)
        
        # Add jitter option in same row to save space
        jitter_container = QHBoxLayout()
        jitter_label = QLabel("Add Jitter")
        jitter_label.setObjectName("smallLabel")
        
        self.jitter_checkbox = QCheckBox()
        self.jitter_checkbox.setChecked(False)
        self.jitter_checkbox.stateChanged.connect(self.update_jitter)
        
        jitter_container.addWidget(jitter_label)
        jitter_container.addWidget(self.jitter_checkbox)
        jitter_container.setSpacing(2)
        
        # Add buttons and jitter to row
        position_row.addWidget(current_btn, 1)
        position_row.addWidget(random_btn, 1)
        position_row.addStretch(1)
        position_row.addLayout(jitter_container)
        
        position_section.addLayout(position_row)
        
        # -- Time Controls Section (replaces Interval Section) --
        time_controls_frame = QFrame()
        time_controls_frame.setObjectName("transparentFrame")
        time_controls_layout = QHBoxLayout(time_controls_frame)
        time_controls_layout.setContentsMargins(0, 8, 0, 0)  # Add some top margin
        
        # Delay between clicks
        delay_container = QHBoxLayout()
        delay_label = QLabel("Delay")
        
        # SpinBox for delay input
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setMinimum(50)
        self.delay_spinbox.setMaximum(5000)
        self.delay_spinbox.setValue(500)  # Default value: 500 ms
        self.delay_spinbox.setSuffix(" ms")
        self.delay_spinbox.setFixedWidth(100)
        self.delay_spinbox.valueChanged.connect(self.update_click_delay)
        
        delay_container.addWidget(delay_label)
        delay_container.addWidget(self.delay_spinbox)
        
        # Total time limit
        limit_container = QHBoxLayout()
        limit_label = QLabel("Limit")
        
        # SpinBox for time limit input
        self.limit_spinbox = QSpinBox()
        self.limit_spinbox.setMinimum(0)
        self.limit_spinbox.setMaximum(3600)
        self.limit_spinbox.setValue(0)  # Default value: 0 seconds (no limit)
        self.limit_spinbox.setSuffix(" sec")
        self.limit_spinbox.setFixedWidth(100)
        self.limit_spinbox.valueChanged.connect(self.update_click_limit)
        
        limit_container.addWidget(limit_label)
        limit_container.addWidget(self.limit_spinbox)
        
        # Add both controls to the same row with a spacer between them
        time_controls_layout.addLayout(delay_container)
        time_controls_layout.addStretch(1)
        time_controls_layout.addLayout(limit_container)
        
        # Add all sections to main layout
        layout.addLayout(type_section)
        layout.addLayout(position_section)
        layout.addWidget(time_controls_frame)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Add custom styles for compact buttons
        self.setStyleSheet("""
            QPushButton#compactButton {
                background-color: #1E1E1E;
                color: #E1E1E1;
                border: 1px solid #31303A;
                border-radius: 6px;
                padding: 2px 4px;
                font-size: 11px;
                min-width: 40px;
            }
            
            QPushButton#compactButton:hover {
                background-color: #2A2A2A;
                border: 1px solid #6750A4;
            }
            
            QPushButton#compactButton:checked {
                background-color: #31303A;
                border: 1px solid #6750A4;
                color: #D0BCFF;
            }
            
            QLabel#smallLabel {
                font-size: 11px;
            }
        """)
    
    def update_click_type(self, button):
        """Update the click type based on button selection"""
        button_id = self.type_group.id(button)
        if button_id == 1:
            update_click_type("left")
        elif button_id == 2:
            update_click_type("right")
        elif button_id == 3:
            update_click_type("double")
        elif button_id == 4:
            update_click_type("middle")
    
    def update_position(self, button):
        """Update the click position based on button selection"""
        button_id = self.position_group.id(button)
        if button_id == 1:
            update_position("current")
        elif button_id == 2:
            update_position("random")
    
    def update_click_delay(self, value):
        """Update the delay between clicks"""
        update_delay(value)
    
    def update_click_limit(self, value):
        """Update the total clicking time limit"""
        update_limit(value)
    
    def update_jitter(self, state):
        """Enable or disable jitter based on checkbox state"""
        update_jitter(state == Qt.CheckState.Checked.value)
    
    def get_current_settings(self):
        """Return current click settings"""
        # Determine click type
        button_id = self.type_group.checkedId()
        if button_id == 1:
            click_type = "left"
        elif button_id == 2:
            click_type = "right"
        elif button_id == 3:
            click_type = "double"
        else:
            click_type = "middle"
            
        # Determine position type
        position_button = self.position_group.checkedButton()
        position_id = self.position_group.id(position_button)
        position = "current" if position_id == 1 else "random"
        
        return {
            'interval': self.delay_spinbox.value() / 1000.0,  # Convert ms to seconds for compatibility
            'click_type': click_type,
            'position': position,
            'jitter': self.jitter_checkbox.isChecked(),
            'delay': self.delay_spinbox.value(),
            'limit': self.limit_spinbox.value()
        }