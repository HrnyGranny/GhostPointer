from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout)
from PyQt6.QtGui import QFont, QKeySequence, QShortcut, QIcon
from PyQt6.QtCore import Qt, pyqtSignal
import os

from src.functions.mouse import start_mouse_drift, stop_mouse_drift
from src.functions.click import start_auto_click, stop_auto_click
from src.gui.mouse import MouseTab
from src.gui.click import ClickTab
from src.gui.assets import get_icon
from src.gui.components import CustomTabWidget, IconButton, HelpButton
from src.gui.console import ConsoleOutput
from src.gui.styles import get_app_styles

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
        
        # Añadir botón de ayuda con posición absoluta
        self.help_button = HelpButton(self)
        # Posicionar en la esquina superior derecha (16px de margen)
        self.help_button.setGeometry(self.width() - 40, 16, 24, 24)
        self.help_button.clicked.connect(self.show_help)

    def apply_styles(self):
        # Aplicar estilos desde el módulo de estilos
        self.setStyleSheet(get_app_styles())

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
        
        # Add elements to the main layout
        self.main_layout.addLayout(top_layout)
        self.main_layout.addLayout(tab_container)
        self.main_layout.addWidget(self.console)
        
        self.setLayout(self.main_layout)

    def show_help(self):
        """Muestra el diálogo de ayuda"""
        # Implementaremos esto más adelante
        if self.dev_mode:
            self.console.log("Help button clicked - feature coming soon")

    def toggle_dev_mode(self, enabled):
        """Activate or deactivate developer mode"""
        self.dev_mode = enabled
        self.console.setVisible(enabled)
        
        # Ajustar el tamaño de la ventana según el modo
        if enabled:
            self.setFixedSize(*self.dev_mode_size)
            # Reposicionar el botón de ayuda al cambiar el tamaño
            self.help_button.setGeometry(self.width() - 40, 16, 24, 24)
            self.console.show_banner()
        else:
            self.setFixedSize(*self.normal_size)
            # Reposicionar el botón de ayuda al cambiar el tamaño
            self.help_button.setGeometry(self.width() - 40, 16, 24, 24)
            self.console.log("Developer mode deactivated.")

    def resizeEvent(self, event):
        """Se ejecuta cuando se cambia el tamaño de la ventana"""
        super().resizeEvent(event)
        # Asegurarse de que el botón de ayuda permanezca en la esquina superior derecha
        self.help_button.setGeometry(self.width() - 40, 16, 24, 24)

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
            
            else:  # Click tab
                # Get current settings from click tab
                settings = self.click_tab.get_current_settings()
                
                # Start auto-clicking with parameters
                start_auto_click(
                    interval=settings['interval'],
                    click_method=settings['click_type'],
                    position=settings['position'],
                    jitter=settings['jitter']
                )
                
                # Log in console
                if self.dev_mode:
                    limit_info = ""
                    if settings['infinite']:
                        limit_info = " (infinite)"
                    elif settings['limit_clicks'] > 0:
                        limit_info = f" (limit: {settings['limit_clicks']} clicks)"
                    elif settings['limit_time'] > 0:
                        limit_info = f" (limit: {settings['limit_time']} seconds)"
                    
                    self.console.log(f"Auto-click started: {settings['click_type']} clicks every {settings['interval']}s{limit_info}")
            
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