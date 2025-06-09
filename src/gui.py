from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QTabWidget, QHBoxLayout, QSlider, QGroupBox,
                             QRadioButton, QCheckBox, QGridLayout, QSpacerItem,
                             QFrame, QButtonGroup, QTextEdit, QSplitter)
from PyQt6.QtGui import QFont, QIcon, QColor, QPainter, QPainterPath, QBrush, QKeySequence, QShortcut
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QPoint, QRect
from mouse_controller import start_mouse_drift, stop_mouse_drift

# Custom Switch Button implementation
class QSwitchButton(QWidget):
    toggled = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(48, 28)
        self.isChecked = False
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # No border
        painter.setPen(Qt.PenStyle.NoPen)
        
        # Draw track
        if self.isChecked:
            track_color = QColor("#6750A4")
            track_opacity = 0.5
        else:
            track_color = QColor("#757575")
            track_opacity = 0.3
            
        track_color.setAlphaF(track_opacity)
        
        track_path = QPainterPath()
        track_path.addRoundedRect(4, 4, 40, 20, 10, 10)
        painter.setBrush(QBrush(track_color))
        painter.drawPath(track_path)
        
        # Draw thumb
        thumb_x = 24 if self.isChecked else 4
        
        # Draw shadow
        shadow_color = QColor(0, 0, 0, 30)
        shadow_path = QPainterPath()
        shadow_path.addEllipse(thumb_x + 2, 6, 18, 18)
        painter.setBrush(QBrush(shadow_color))
        painter.drawPath(shadow_path)
        
        # Draw thumb
        if self.isChecked:
            thumb_color = QColor("#6750A4")
        else:
            thumb_color = QColor("#FAFAFA")
            
        thumb_path = QPainterPath()
        thumb_path.addEllipse(thumb_x, 4, 20, 20)
        painter.setBrush(QBrush(thumb_color))
        painter.drawPath(thumb_path)
        
        # Draw icons inside thumb
        if self.isChecked:
            # Developer mode icon
            painter.setPen(QColor("#FFFFFF"))
            painter.drawText(QRect(thumb_x + 4, 4, 12, 20), Qt.AlignmentFlag.AlignCenter, "⚙️")
        else:
            # User mode icon
            painter.setPen(QColor("#6750A4"))
            painter.drawText(QRect(thumb_x + 4, 4, 12, 20), Qt.AlignmentFlag.AlignCenter, "👤")
        
    def mousePressEvent(self, event):
        self.toggle()
        
    def toggle(self):
        self.isChecked = not self.isChecked
        self.update()
        self.toggled.emit(self.isChecked)

class CustomTabWidget(QTabWidget):
    modeToggled = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create switch
        self.mode_switch = QSwitchButton(self)
        
        # Connect switch signal
        self.mode_switch.toggled.connect(self.toggle_mode)
        
        # Set side margins for the tab bar
        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                border-radius: 12px;
                background-color: #1E1E1E;
                margin-top: 4px;
            }
            
            QTabBar {
                padding-left: 30px;
            }
            
            QTabBar::tab {
                background-color: transparent;
                color: #B0B0B0;
                border: none;
                border-radius: 6px;
                min-width: 100px;
                padding: 8px 16px;
                margin-right: 4px;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-size: 11px;
            }
            
            QTabBar::tab:selected {
                background-color: #6750A4;
                color: white;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: rgba(103, 80, 164, 0.1);
                color: #D0BCFF;
            }
        """)
        
    def toggle_mode(self, enabled):
        # Emit the signal so GhostPointerGUI can handle the console
        self.modeToggled.emit(enabled)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Position the switch to the right of the tabs
        tabbar_height = self.tabBar().height()
        
        # Position the switch
        switch_width = self.mode_switch.width()
        
        # Right margin
        right_margin = 12  # Increased to compensate for content margin
        
        # Position the switch
        self.mode_switch.move(
            self.width() - switch_width - right_margin,
            (tabbar_height - self.mode_switch.height()) // 2
        )

class MaterialButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setObjectName("materialButton")

class ConsoleOutput(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setObjectName("consoleOutput")
        self.setMinimumHeight(120)
        self.setMaximumHeight(200)
        
    def log(self, message):
        """Add a message to the console"""
        self.append(f"> {message}")

class GhostPointerGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Main window configuration
        self.setWindowTitle("👻 GhostPointer")
        self.setMinimumSize(550, 500)  # Fixed minimum size
        self.is_moving = False
        self.dev_mode = False
        self.setup_ui()

    def setup_ui(self):
        # Material Design compact style
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #E1E1E1;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 12px;
            }
            
            #materialButton {
                background-color: #6750A4;
                color: white;
                border: none;
                border-radius: 40px;
                font-size: 15px;
                font-weight: 600;
                padding: 12px;
            }
            
            #materialButton:hover {
                background-color: #7965B5;
            }
            
            #materialButton:pressed {
                background-color: #5E47A1;
            }
            
            QPushButton#optionButton {
                background-color: #1E1E1E;
                color: #E1E1E1;
                border: 1px solid #31303A;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: 500;
                min-height: 32px;
            }
            
            QPushButton#optionButton:hover {
                background-color: #2A2A2A;
                border: 1px solid #6750A4;
            }
            
            QPushButton#optionButton:checked {
                background-color: #31303A;
                border: 1px solid #6750A4;
                color: #D0BCFF;
            }
            
            QSlider::groove:horizontal {
                border: none;
                height: 4px;
                background: #31303A;
                margin: 0;
                border-radius: 2px;
            }
            
            QSlider::handle:horizontal {
                background: #6750A4;
                border: none;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            
            QSlider::handle:horizontal:hover {
                background: #7965B5;
                width: 18px;
                height: 18px;
                margin: -7px 0;
                border-radius: 9px;
            }
            
            QFrame#optionsFrame {
                border: 1px solid #31303A;
                border-radius: 10px;
                background-color: #1A1A1A;
            }
            
            QCheckBox {
                spacing: 6px;
                min-height: 26px;
                padding-left: 4px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            
            QCheckBox::indicator::unchecked {
                border: 2px solid #7A7289;
                background: transparent;
                border-radius: 4px;
            }
            
            QCheckBox::indicator::checked {
                border: 2px solid #6750A4;
                background: #6750A4;
                border-radius: 4px;
            }
            
            QCheckBox:hover {
                color: #D0BCFF;
                background-color: rgba(208, 188, 255, 0.08);
                border-radius: 6px;
            }
            
            QLabel#shortcutLabel {
                color: #8F8F8F;
                font-size: 11px;
                font-style: italic;
                font-weight: 400;
                margin-top: 4px;
            }
            
            #consoleOutput {
                background-color: #1A1A1A;
                border: 1px solid #31303A;
                border-radius: 8px;
                color: #E1E1E1;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                padding: 8px;
            }
        """)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(16, 16, 16, 16)

        # Top section with main button
        top_layout = QVBoxLayout()
        
        # Main button (with play icon)
        button_container = QHBoxLayout()
        button_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.main_button = MaterialButton("▶")  # Play icon
        self.main_button.setFixedSize(90, 90)
        self.main_button.setFont(QFont("Segoe UI", 32))
        self.main_button.clicked.connect(self.toggle_movement)
        
        button_container.addWidget(self.main_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Shortcut key label
        self.shortcut_label = QLabel("Ctrl+Space to start")
        self.shortcut_label.setObjectName("shortcutLabel")
        self.shortcut_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add keyboard shortcut (Ctrl+Space)
        self.toggle_shortcut = QShortcut(QKeySequence("Ctrl+Space"), self)
        self.toggle_shortcut.activated.connect(self.toggle_movement)
        
        top_layout.addLayout(button_container)
        top_layout.addWidget(self.shortcut_label)

        # Container for TabWidget with specific padding
        tab_container = QVBoxLayout()
        tab_container.setContentsMargins(0, 0, 0, 0)  # No additional margins
        
        # Tabs section with integrated switch
        self.tab_widget = CustomTabWidget()
        self.tab_widget.modeToggled.connect(self.toggle_dev_mode)
        
        # Tab 1: Mouse Movement
        self.movement_tab = QWidget()
        self.setup_tab_content(self.movement_tab, "Movement")
        self.tab_widget.addTab(self.movement_tab, "Movement")
        
        # Tab 2: Click
        self.click_tab = QWidget()
        self.setup_tab_content(self.click_tab, "Click")
        self.tab_widget.addTab(self.click_tab, "Click")
        
        # Tab 3: Movement and Click
        self.combined_tab = QWidget()
        self.setup_tab_content(self.combined_tab, "Movement and Click")
        self.tab_widget.addTab(self.combined_tab, "Movement and Click")
        
        tab_container.addWidget(self.tab_widget)
        
        # Developer console (hidden by default)
        self.console = ConsoleOutput()
        self.console.setVisible(False)
        self.console.log("Developer console initialized.")
        self.console.log("Use this console to debug and receive event information.")
        
        # Add elements to the main layout
        self.main_layout.addLayout(top_layout)
        self.main_layout.addLayout(tab_container)
        self.main_layout.addWidget(self.console)
        
        self.setLayout(self.main_layout)

    def setup_tab_content(self, tab, title):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Button section (Random/Record)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        # Button group for exclusivity
        button_group = QButtonGroup(tab)
        
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
        
        # Options frame
        options_frame = QFrame()
        options_frame.setObjectName("optionsFrame")
        options_layout = QVBoxLayout(options_frame)
        options_layout.setContentsMargins(12, 12, 12, 12)
        options_layout.setSpacing(8)
        
        # Add 2 options as checkboxes
        option1 = QCheckBox("Option 1")
        option2 = QCheckBox("Option 2")
        
        options_layout.addWidget(option1)
        options_layout.addWidget(option2)
        
        # Speed section
        speed_layout = QVBoxLayout()
        speed_layout.setContentsMargins(0, 8, 0, 0)
        
        speed_label = QLabel("Speed")
        speed_label.setObjectName("sectionLabel")
        
        speed_slider = QSlider(Qt.Orientation.Horizontal)
        speed_slider.setMinimum(1)
        speed_slider.setMaximum(10)
        speed_slider.setValue(5)
        
        value_label = QLabel("5")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(speed_slider)
        speed_layout.addWidget(value_label)
        
        # Add all elements to the tab's main layout
        layout.addLayout(button_layout)
        layout.addWidget(options_frame)
        layout.addLayout(speed_layout)
        layout.addStretch()
        
        tab.setLayout(layout)
        
    def toggle_dev_mode(self, enabled):
        """Activate or deactivate developer mode"""
        self.dev_mode = enabled
        self.console.setVisible(enabled)
        
        if enabled:
            self.console.log("Developer mode activated.")
        else:
            self.console.log("Developer mode deactivated.")
        
        # Adjust window size if necessary
        self.adjustSize()

    def toggle_movement(self):
        if not self.is_moving:
            # Starting movement
            start_mouse_drift()
            # Change to STOP icon (square)
            self.main_button.setText("■")
            self.main_button.setStyleSheet("""
                background-color: #F44336; 
                color: white; 
                border: none; 
                border-radius: 45px;
                font-size: 32px;
                font-weight: 600;
                padding: 12px;
            """)
            # Update shortcut text
            self.shortcut_label.setText("Ctrl+Space to stop")
            
            # Log in console
            if self.dev_mode:
                self.console.log("Mouse movement started.")
        else:
            # Stopping movement
            stop_mouse_drift()
            # Change to PLAY icon (triangle)
            self.main_button.setText("▶")
            self.main_button.setStyleSheet("""
                background-color: #6750A4; 
                color: white; 
                border: none; 
                border-radius: 45px;
                font-size: 32px;
                font-weight: 600;
                padding: 12px;
            """)
            # Update shortcut text
            self.shortcut_label.setText("Ctrl+Space to start")
            
            # Log in console
            if self.dev_mode:
                self.console.log("Mouse movement stopped.")
        
        # Change state
        self.is_moving = not self.is_moving