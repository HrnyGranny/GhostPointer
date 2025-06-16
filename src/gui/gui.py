from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QTabWidget, QHBoxLayout, QTextEdit)
from PyQt6.QtGui import QFont, QKeySequence, QShortcut, QPainter, QPainterPath, QBrush, QColor, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QSize
import os

from src.functions.mouse import start_mouse_drift, stop_mouse_drift
from src.functions.click import start_auto_click, stop_auto_click
from src.gui.mouse import MouseTab
from src.gui.click import ClickTab
from src.gui.assets import get_icon

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

class IconButton(QPushButton):
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(90, 90))
        self.setFixedSize(90, 90)
        # Remove all button styling to show only the icon
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: transparent;
            }
            QPushButton:pressed {
                background-color: transparent;
            }
        """)
        # Make the button flat
        self.setFlat(True)

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
        
        # Tamaños para los diferentes modos
        self.normal_size = (390, 400)
        self.dev_mode_size = (390, 600)
        
        # Inicialmente configuramos tamaño fijo para modo normal
        self.setFixedSize(*self.normal_size)  # Usar setFixedSize para bloquear redimensionamiento
        
        # Establecer flags de ventana para que no se pueda redimensionar
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        
        self.is_moving = False
        self.dev_mode = False

        # Initialize state variables
        self.is_moving = False
        self.dev_mode = False
        
        # Define paths to icon files
        self.play_icon_path = get_icon('Play.png')
        self.stop_icon_path = get_icon('Stop.png')
        
        self.setup_ui()
        self.apply_styles()

    def apply_styles(self):
        # Material Design compact style
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #E1E1E1;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 12px;
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
            
            QFrame#optionsFrameWithBg {
                border: 1px solid #31303A;
                border-radius: 10px;
                background-color: #1A1A1A;
            }
            
            QFrame#transparentFrame {
                border: none;
                background-color: transparent;
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
            
            QSpinBox {
                background-color: #2A2A2A;
                border: 1px solid #31303A;
                border-radius: 4px;
                padding: 2px 8px;
                color: #E1E1E1;
            }
            
            QSpinBox:hover {
                border: 1px solid #6750A4;
            }
            
            QSpinBox::up-button, QSpinBox::down-button {
                width: 16px;
                border-radius: 2px;
                background-color: #3A3A3A;
            }
            
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #6750A4;
            }
            
            QLabel#speedValueLabel {
                color: #D0BCFF;
                font-weight: bold;
                font-size: 14px;
            }
            
            QLabel#smoothLabel {
                color: #E1E1E1;
                padding-right: 0px;
            }
        """)

    def setup_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(16, 16, 16, 16)

        # Top section with main button
        top_layout = QVBoxLayout()
        
        # Main button (with play icon)
        button_container = QHBoxLayout()
        button_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create main button with play icon from PNG
        self.main_button = IconButton(self.play_icon_path)
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
        
        # Tab 1: Mouse Movement (now using MouseTab class)
        self.movement_tab = MouseTab()
        self.tab_widget.addTab(self.movement_tab, "Movement")
        
        # Tab 2: Click (now using ClickTab class)
        self.click_tab = ClickTab()
        self.tab_widget.addTab(self.click_tab, "Click")
        
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

    def toggle_dev_mode(self, enabled):
        """Activate or deactivate developer mode"""
        self.dev_mode = enabled
        self.console.setVisible(enabled)
        
        # Ajustar el tamaño de la ventana según el modo
        if enabled:
            self.setFixedSize(*self.dev_mode_size)
            self.console.log("Developer mode activated.")
        else:
            self.setFixedSize(*self.normal_size)
            self.console.log("Developer mode deactivated.")

    def toggle_movement(self):
        """Start or stop the current action based on the active tab"""
        if not self.is_moving:
            # Determine which tab is active
            current_tab_index = self.tab_widget.currentIndex()
            
            if current_tab_index == 0:  # Movement tab
                # Get current settings from mouse tab
                settings = self.movement_tab.get_current_settings()
                
                # Starting movement with parameters
                start_mouse_drift(
                    speed=settings['speed'], 
                    delay=settings['delay']
                )
                
                # Log in console
                if self.dev_mode:
                    self.console.log(f"Mouse movement started with speed={settings['speed']}, delay={settings['delay']}ms")
            
            else:  
                # Get current settings from click tab
                settings = self.click_tab.get_current_settings()
                
                # Start auto-clicking with parameters
                start_auto_click(
                    interval=settings['interval'],
                    click_method=settings['click_type'],
                    position=settings['position'],
                    jitter=settings['jitter'],
                    delay=settings['delay'],
                    limit=settings['limit']
                )
                                
                # Log in console
                if self.dev_mode:
                    self.console.log(f"Auto-click started: {settings['click_type']} clicks every {settings['interval']}s")
            
            # Change to STOP icon
            self.main_button.setIcon(QIcon(self.stop_icon_path))
            # Update shortcut text
            self.shortcut_label.setText("Ctrl+Space to stop")
            
        else:
            # Determine which tab is active
            current_tab_index = self.tab_widget.currentIndex()
            
            if current_tab_index == 0:  # Movement tab
                # Stopping movement
                stop_mouse_drift()
                
                # Log in console
                if self.dev_mode:
                    self.console.log("Mouse movement stopped.")
            
            else:  # Click tab
                # Stopping auto-click
                stop_auto_click()
                
                # Log in console
                if self.dev_mode:
                    self.console.log("Auto-click stopped.")
            
            # Change to PLAY icon
            self.main_button.setIcon(QIcon(self.play_icon_path))
            # Update shortcut text
            self.shortcut_label.setText("Ctrl+Space to start")
        
        # Change state
        self.is_moving = not self.is_moving