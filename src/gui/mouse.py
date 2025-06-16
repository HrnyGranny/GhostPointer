from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QSlider, QFrame, QButtonGroup,
                             QCheckBox, QSpinBox)
from PyQt6.QtCore import Qt
from src.functions.mouse import update_speed, update_delay

class MouseTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup for the movement tab with transparent options"""
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 8)  # Reduced bottom margin
        layout.setSpacing(6)  # Reduced spacing
        
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
        button_layout.addWidget(random_btn, 1)  # 1 indicates proportional space
        button_layout.addWidget(record_btn, 1)
        
        # Options section with transparent background
        options_frame = QFrame()
        options_frame.setObjectName("transparentFrame")  # Transparent frame
        options_layout = QHBoxLayout(options_frame)  # Changed to HBoxLayout for a single row
        options_layout.setContentsMargins(2, 16, 2, 2)  # Minimal padding
        
        # Delay option with spinbox
        delay_label = QLabel("Delay")
        
        # SpinBox for delay input
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setMinimum(0)
        self.delay_spinbox.setMaximum(5000)
        self.delay_spinbox.setValue(1000)  # Default value: 1000 ms (1 second)
        self.delay_spinbox.setSuffix(" ms")
        self.delay_spinbox.setFixedWidth(100)
        self.delay_spinbox.valueChanged.connect(self.update_delay_value)
        
        # Create container for Smooth label and checkbox
        smooth_container = QHBoxLayout()
        
        # Smooth label - added to the left of checkbox
        smooth_label = QLabel("Smooth")
        smooth_label.setObjectName("smoothLabel")
        
        # Checkbox without text
        self.smooth_checkbox = QCheckBox("")
        self.smooth_checkbox.setChecked(False) 
        
        smooth_container.addWidget(smooth_label)
        smooth_container.addWidget(self.smooth_checkbox)
        smooth_container.setSpacing(2)  # Minimal spacing between label and checkbox
        
        # Add all options to the layout
        options_layout.addWidget(delay_label)
        options_layout.addWidget(self.delay_spinbox)
        options_layout.addStretch(1)  # Stretch to push the smooth option to the right
        options_layout.addLayout(smooth_container)
        
        # Speed section
        speed_layout = QVBoxLayout()
        speed_layout.setContentsMargins(0, 9, 0, 0)  # Reduced top margin

        speed_header_layout = QHBoxLayout()
        speed_label = QLabel("Speed")
        speed_label.setObjectName("sectionLabel")
        
        # Live speed value display
        self.speed_value_label = QLabel("25")  # Default value: 25
        self.speed_value_label.setObjectName("speedValueLabel")
        self.speed_value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        speed_header_layout.addWidget(speed_label)
        speed_header_layout.addStretch()
        speed_header_layout.addWidget(self.speed_value_label)
        
        # Speed slider
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(25)  # Default value: 25
        
        # Connect slider value changes to update the label
        self.speed_slider.valueChanged.connect(self.update_speed_value)
        
        speed_layout.addLayout(speed_header_layout)
        speed_layout.addWidget(self.speed_slider)
        
        # Add all elements to the tab's main layout
        layout.addLayout(button_layout)
        layout.addWidget(options_frame)
        layout.addLayout(speed_layout)
        # No stretch to minimize space at bottom

        layout.addStretch(1)
        
        self.setLayout(layout)
    
    def update_speed_value(self, value):
        """Update the speed value label when slider changes and notify the mouse controller"""
        self.speed_value_label.setText(str(value))
        update_speed(value)
    
    def update_delay_value(self, value):
        """Update the delay between mouse movements"""
        update_delay(value)
    
    def get_current_settings(self):
        """Return current mouse movement settings"""
        return {
            'speed': self.speed_slider.value(),
            'delay': self.delay_spinbox.value(),
            'smooth': self.smooth_checkbox.isChecked()
        }