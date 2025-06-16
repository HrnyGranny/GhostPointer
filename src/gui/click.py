from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QButtonGroup, QFrame,
                             QSlider, QDoubleSpinBox, QCheckBox)
from PyQt6.QtCore import Qt
from src.functions.click import update_interval, update_click_type, update_position, update_jitter

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
            btn.setFixedHeight(28)  # Altura reducida
        
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
            btn.setFixedHeight(28)  # Altura reducida
        
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
        
        # Add buttons and jitter to row - CORRECCIÓN: argumento de addStretch debe ser int, no float
        position_row.addWidget(current_btn, 1)
        position_row.addWidget(random_btn, 1)
        position_row.addStretch(1)  # Cambiado de 0.5 a 1
        position_row.addLayout(jitter_container)
        
        position_section.addLayout(position_row)
        
        # -- Interval Section --
        interval_frame = QFrame()
        interval_frame.setObjectName("transparentFrame")
        interval_layout = QVBoxLayout(interval_frame)
        interval_layout.setContentsMargins(0, 0, 0, 0)
        interval_layout.setSpacing(4)
        
        interval_header = QHBoxLayout()
        interval_label = QLabel("Click Interval")
        interval_label.setObjectName("sectionLabel")
        
        # Display for interval value
        self.interval_value_label = QLabel("1.0 sec")
        self.interval_value_label.setObjectName("valueLabel")
        self.interval_value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        interval_header.addWidget(interval_label)
        interval_header.addStretch()
        interval_header.addWidget(self.interval_value_label)
        
        # Controls for interval
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)
        
        # SpinBox for precise interval input
        self.interval_spinbox = QDoubleSpinBox()
        self.interval_spinbox.setMinimum(0.1)
        self.interval_spinbox.setMaximum(10.0)
        self.interval_spinbox.setValue(1.0)
        self.interval_spinbox.setSingleStep(0.1)
        self.interval_spinbox.setSuffix(" sec")
        self.interval_spinbox.setFixedWidth(80)
        self.interval_spinbox.valueChanged.connect(self.update_interval_value)
        
        # Slider for quick interval adjustment
        self.interval_slider = QSlider(Qt.Orientation.Horizontal)
        self.interval_slider.setMinimum(1)  # 0.1 seconds
        self.interval_slider.setMaximum(100)  # 10 seconds
        self.interval_slider.setValue(10)  # 1.0 seconds
        self.interval_slider.setTickPosition(QSlider.TickPosition.NoTicks)
        self.interval_slider.valueChanged.connect(self.sync_slider_to_spinbox)
        
        controls_layout.addWidget(self.interval_spinbox)
        controls_layout.addWidget(self.interval_slider, 1)
        
        interval_layout.addLayout(interval_header)
        interval_layout.addLayout(controls_layout)
        
        # Add all sections to main layout
        layout.addLayout(type_section)
        layout.addLayout(position_section)
        layout.addWidget(interval_frame)
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
    
    def update_interval_value(self, value):
        """Update the interval value and synchronize slider"""
        self.interval_value_label.setText(f"{value:.1f} sec")
        
        # Update slider without triggering its valueChanged signal
        self.interval_slider.blockSignals(True)
        self.interval_slider.setValue(int(value * 10))
        self.interval_slider.blockSignals(False)
        
        # Update the clicking function
        update_interval(value)
    
    def sync_slider_to_spinbox(self, value):
        """Convert slider value to interval and update spinbox"""
        # Convert slider value (1-100) to seconds (0.1-10.0)
        interval = value / 10.0
        
        # Update spinbox without triggering its valueChanged signal
        self.interval_spinbox.blockSignals(True)
        self.interval_spinbox.setValue(interval)
        self.interval_spinbox.blockSignals(False)
        
        # Update the display label and clicking function
        self.interval_value_label.setText(f"{interval:.1f} sec")
        update_interval(interval)
    
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
        button_id = self.position_group.id(button)
        position = "current" if button_id == 1 else "random"
        
        return {
            'interval': self.interval_spinbox.value(),
            'click_type': click_type,
            'position': position,
            'jitter': self.jitter_checkbox.isChecked()
        }