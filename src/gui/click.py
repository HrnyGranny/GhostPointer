from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QButtonGroup, QFrame,
                             QSpinBox, QCheckBox, QRadioButton)
from PyQt6.QtCore import Qt, QPoint
from src.functions.click import update_click_type, update_position, update_jitter, update_delay, update_limit, set_specific_position, needs_position_selection
from src.functions.position_selector import PositionSelectorOverlay

class ClickTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_position = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup for the click tab with new layout structure"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 8, 16, 8)
        main_layout.setSpacing(12)
        
        # --- ROW 1: Click Type and Position ---
        top_row_layout = QHBoxLayout()
        
        # Left side - Click Type
        type_container = QVBoxLayout()
        type_label = QLabel("Click Type")
        type_label.setObjectName("sectionLabel")
        type_container.setSpacing(5)
        
        type_buttons = QHBoxLayout()
        type_buttons.setSpacing(6)
        
        # Create button group for click type
        self.type_group = QButtonGroup(self)
        self.type_group.setExclusive(True)
        
        # Create Left/Right buttons
        left_btn = QPushButton("Left")
        right_btn = QPushButton("Right")
        
        for btn in [left_btn, right_btn]:
            btn.setObjectName("compactButton")
            btn.setCheckable(True)
            btn.setFixedHeight(28)
        
        left_btn.setChecked(True)
        
        self.type_group.addButton(left_btn, 1)
        self.type_group.addButton(right_btn, 2)
        self.type_group.buttonClicked.connect(self.update_click_type)
        
        type_buttons.addWidget(left_btn)
        type_buttons.addWidget(right_btn)
        type_buttons.addStretch()
        
        type_container.addWidget(type_label)
        type_container.addLayout(type_buttons)
        
        # Right side - Click Position
        position_container = QVBoxLayout()
        position_label = QLabel("Click Position")
        position_label.setObjectName("sectionLabel")
        position_container.setSpacing(5)
        
        position_buttons = QHBoxLayout()
        position_buttons.setSpacing(6)
        
        # Create button group for position
        self.position_group = QButtonGroup(self)
        self.position_group.setExclusive(True)
        
        current_btn = QPushButton("Current")
        select_btn = QPushButton("Select")
        
        for btn in [current_btn, select_btn]:
            btn.setObjectName("compactButton")
            btn.setCheckable(True)
            btn.setFixedHeight(28)
        
        current_btn.setChecked(True)
        
        self.position_group.addButton(current_btn, 1)
        self.position_group.addButton(select_btn, 2)
        self.position_group.buttonClicked.connect(self.update_position)
        
        position_buttons.addWidget(current_btn)
        position_buttons.addWidget(select_btn)
        position_buttons.addStretch()
        
        position_container.addWidget(position_label)
        position_container.addLayout(position_buttons)
        
        # Add both sections to the top row with a separator in between
        top_row_layout.addLayout(type_container, 1)
        top_row_layout.addSpacing(20)  # Separation between sections
        top_row_layout.addLayout(position_container, 1)
        
        # --- ROW 2: Delay and Jitter ---
        middle_frame = QFrame()
        middle_frame.setObjectName("transparentFrame")
        middle_layout = QHBoxLayout(middle_frame)
        middle_layout.setContentsMargins(0, 0, 0, 0)
        
        # Delay controls
        delay_container = QVBoxLayout()
        delay_label = QLabel("Delay")
        delay_label.setObjectName("sectionLabel")
        
        delay_inputs = QHBoxLayout()
        
        # Minutes input - SAME WIDTH (90px)
        self.delay_min_spinbox = QSpinBox()
        self.delay_min_spinbox.setMinimum(0)
        self.delay_min_spinbox.setMaximum(60)
        self.delay_min_spinbox.setValue(0)
        self.delay_min_spinbox.setSuffix(" min")
        self.delay_min_spinbox.setFixedWidth(90)
        self.delay_min_spinbox.valueChanged.connect(self.update_delay_values)
        
        # Seconds input - SAME WIDTH (90px)
        self.delay_sec_spinbox = QSpinBox()
        self.delay_sec_spinbox.setMinimum(0)
        self.delay_sec_spinbox.setMaximum(59)
        self.delay_sec_spinbox.setValue(1)
        self.delay_sec_spinbox.setSuffix(" sec")
        self.delay_sec_spinbox.setFixedWidth(90)
        self.delay_sec_spinbox.valueChanged.connect(self.update_delay_values)
        
        delay_inputs.addWidget(self.delay_min_spinbox)
        delay_inputs.addWidget(self.delay_sec_spinbox)
        delay_inputs.addStretch()
        
        delay_container.addWidget(delay_label)
        delay_container.addLayout(delay_inputs)
        
        # Jitter checkbox on the right
        jitter_container = QVBoxLayout()
        jitter_container.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        # Spacer to align with inputs
        jitter_spacer = QVBoxLayout()
        jitter_spacer.addStretch()
        
        jitter_check_layout = QHBoxLayout()
        jitter_label = QLabel("Add Jitter")
        jitter_label.setObjectName("sectionLabel")
        
        self.jitter_checkbox = QCheckBox()
        self.jitter_checkbox.setChecked(False)
        self.jitter_checkbox.stateChanged.connect(self.update_jitter)
        
        jitter_check_layout.addWidget(jitter_label)
        jitter_check_layout.addWidget(self.jitter_checkbox)
        jitter_check_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        jitter_container.addLayout(jitter_spacer)
        jitter_container.addLayout(jitter_check_layout)
        
        middle_layout.addLayout(delay_container, 3)
        middle_layout.addLayout(jitter_container, 1)
        
        # --- ROW 3: Limit with Radio Buttons and Single Box ---
        bottom_frame = QFrame()
        bottom_frame.setObjectName("transparentFrame")
        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(5)
        
        # Main limit container
        limit_main_container = QHBoxLayout()
        
        # Left side - Limit label and radio buttons
        limit_left_container = QVBoxLayout()
        limit_label = QLabel("Limit")
        limit_label.setObjectName("sectionLabel")
        
        # Radio button group in horizontal layout
        radio_layout = QHBoxLayout()
        radio_layout.setSpacing(14)  # Spacing between radio buttons
        
        # Create radio buttons and group
        self.limit_group = QButtonGroup(self)
        
        clicks_radio = QRadioButton("Clicks")
        time_radio = QRadioButton("Time")
        infinite_radio = QRadioButton("Infinite")
        
        clicks_radio.setChecked(True)  # Default selection
        
        self.limit_group.addButton(clicks_radio, 1)
        self.limit_group.addButton(time_radio, 2)
        self.limit_group.addButton(infinite_radio, 3)
        
        self.limit_group.buttonClicked.connect(self.update_limit_type)
        
        # Add radio buttons to layout
        radio_layout.addWidget(clicks_radio)
        radio_layout.addWidget(time_radio)
        radio_layout.addWidget(infinite_radio)
        radio_layout.addStretch()
        
        # Add label and radio buttons to left container
        limit_left_container.addWidget(limit_label)
        limit_left_container.addLayout(radio_layout)
        
        # Right side - Common input field - MODIFICADO PARA ALINEAR CON RADIO BUTTONS
        limit_right_container = QVBoxLayout()
        
        # Añadir un espaciador para compensar la altura del label "Limit"
        limit_right_container.addSpacing(16) 
        
        # Single common input for both clicks and time
        input_layout = QHBoxLayout()
        
        self.limit_value_spinbox = QSpinBox()
        self.limit_value_spinbox.setMinimum(1)
        self.limit_value_spinbox.setMaximum(99999)
        self.limit_value_spinbox.setValue(100)
        self.limit_value_spinbox.setSuffix(" clicks")  # Default to clicks
        self.limit_value_spinbox.setFixedWidth(110)
        self.limit_value_spinbox.valueChanged.connect(self.update_limit_values)
        
        # Add input to layout
        input_layout.addWidget(self.limit_value_spinbox)
        input_layout.addStretch()
        
        # Add input layout to right container
        limit_right_container.addLayout(input_layout)
        limit_right_container.addStretch()
        
        # Add both containers to main limit container
        limit_main_container.addLayout(limit_left_container, 3)
        limit_main_container.addSpacing(22) 
        limit_main_container.addLayout(limit_right_container, 2)
        
        # Add limit container to bottom layout
        bottom_layout.addLayout(limit_main_container)
        
        # Add all rows to the main layout
        main_layout.addLayout(top_row_layout)
        main_layout.addWidget(middle_frame)
        main_layout.addWidget(bottom_frame)
        main_layout.addStretch()
        
        self.setLayout(main_layout)

    def update_limit_type(self, button):
        """Update limit type and configure the shared spinbox accordingly"""
        button_id = self.limit_group.id(button)
        
        if button_id == 1:  # Clicks
            self.limit_value_spinbox.setEnabled(True)
            self.limit_value_spinbox.setMinimum(1)
            self.limit_value_spinbox.setMaximum(99999)
            self.limit_value_spinbox.setSuffix(" clicks")
            # Keep current value if it's in range
            if self.limit_value_spinbox.value() < 1:
                self.limit_value_spinbox.setValue(100)  # Default for clicks
            self.update_limit_values()
            
        elif button_id == 2:  # Time
            self.limit_value_spinbox.setEnabled(True)
            self.limit_value_spinbox.setMinimum(1)
            self.limit_value_spinbox.setMaximum(3600)
            self.limit_value_spinbox.setSuffix(" sec")
            # Keep current value if it's in range
            if self.limit_value_spinbox.value() > 3600:
                self.limit_value_spinbox.setValue(60)  # Default for time
            self.update_limit_values()
            
        elif button_id == 3:  # Infinite
            self.limit_value_spinbox.setEnabled(False)
            update_limit(0, 0)  # 0 means infinite for both clicks and time
    
    def update_click_type(self, button):
        """Update the click type based on button selection"""
        button_id = self.type_group.id(button)
        if button_id == 1:
            update_click_type("left")
        elif button_id == 2:
            update_click_type("right")
    
    def update_position(self, button):
        """Update the click position based on button selection"""
        button_id = self.position_group.id(button)
        if button_id == 1:
            update_position("current")
            self.selected_position = None
        elif button_id == 2:
            # If "Select" is chosen, reset any previously selected position
            self.selected_position = None
            update_position("select")

    def show_position_selector(self):
        """Muestra el selector de posición en pantalla"""
        self.overlay = PositionSelectorOverlay()
        self.overlay.positionSelected.connect(self.on_position_selected)
        self.overlay.selectionCanceled.connect(self.on_selection_canceled)
        self.overlay.show()
    
    def on_selection_canceled(self):
        """Maneja la cancelación de la selección de posición"""
        # Keep in "Select" mode, don't switch back to "Current"
        pass
    
    def on_position_selected(self, point):
        """Procesa la posición seleccionada"""
        x, y = point.x(), point.y()
        self.selected_position = (x, y)
        
        print(f"Position selected: ({x}, {y})")
        # Actualizar la posición en la lógica de clics
        update_position("specific")
        set_specific_position(x, y)
    
    def update_delay_values(self):
        """Calculate total delay in milliseconds from minutes and seconds"""
        minutes = self.delay_min_spinbox.value()
        seconds = self.delay_sec_spinbox.value()
        
        # Convert to milliseconds (ensure at least 50ms)
        total_ms = max((minutes * 60 + seconds) * 1000, 50)
        update_delay(total_ms)
    
    def update_limit_values(self):
        """Update limit values based on current selection"""
        limit_type = self.limit_group.checkedId()
        value = self.limit_value_spinbox.value()
        
        if limit_type == 1:  # Clicks
            update_limit(value, 0)  # Use clicks, no time limit
        elif limit_type == 2:  # Time
            update_limit(0, value)  # No click limit, use time limit
        # Infinite is handled in update_limit_type
    
    def update_jitter(self, state):
        """Enable or disable jitter based on checkbox state"""
        update_jitter(state == Qt.CheckState.Checked.value)
    
    def needs_position_selection(self):
        """Check if position selection is needed"""
        position_id = self.position_group.checkedId()
        return position_id == 2 and self.selected_position is None
    
    def get_current_settings(self):
        """Return current click settings"""
        # Determine click type
        button_id = self.type_group.checkedId()
        click_type = "left" if button_id == 1 else "right"
            
        # Determine position type
        position_button = self.position_group.checkedButton()
        position_id = self.position_group.id(position_button)
        
        if position_id == 1:
            position = "current"
        else:  # position_id == 2
            position = "select" if self.selected_position is None else "specific"
            
        # Calculate delay
        minutes = self.delay_min_spinbox.value()
        seconds = self.delay_sec_spinbox.value()
        delay_ms = (minutes * 60 + seconds) * 1000
        
        # Determine limit based on selection
        limit_type = self.limit_group.checkedId()
        value = self.limit_value_spinbox.value()
        
        if limit_type == 1:  # Clicks
            clicks = value
            time_limit = 0
            is_infinite = False
        elif limit_type == 2:  # Time
            clicks = 0
            time_limit = value
            is_infinite = False
        else:  # Infinite
            clicks = 0
            time_limit = 0
            is_infinite = True
        
        return {
            'interval': delay_ms / 1000.0,  # Convert ms to seconds for compatibility
            'click_type': click_type,
            'position': position,
            'jitter': self.jitter_checkbox.isChecked(),
            'delay': delay_ms,
            'limit_clicks': clicks,
            'limit_time': time_limit,
            'infinite': is_infinite,
            'limit_type': ['clicks', 'time', 'infinite'][limit_type - 1],
            'specific_position': self.selected_position
        }