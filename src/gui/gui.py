from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame)
from PyQt6.QtGui import QFont, QKeySequence, QShortcut, QIcon, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
import os

from src.functions.mouse import start_mouse_drift, stop_mouse_drift
from src.functions.click import start_auto_click, stop_auto_click
from src.gui.mouse import MouseTab
from src.gui.click import ClickTab
from src.gui.assets import get_icon
from src.gui.components import CustomTabWidget, IconButton, HelpButton
from src.gui.console import ConsoleOutput
from src.gui.contador import ContadorLogic
from src.gui.styles import get_app_styles

class GhostPointerGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        # Tamaños para los diferentes modos (aumentados para incluir el contador)
        self.normal_size = (390, 422)  # 400 + 22 para el contador
        self.dev_mode_size = (390, 622)  # 600 + 22 para el contador
        
        # Inicialmente configuramos tamaño fijo para modo normal
        self.setFixedSize(*self.normal_size)  # Usar setFixedSize para bloquear redimensionamiento
        
        # Establecer flags de ventana para que no se pueda redimensionar
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        
        # Variables de estado
        self.is_moving = False
        self.dev_mode = False
        self.position_selection_pending = False
        
        # Define paths to icon files
        self.play_icon_path = get_icon('Play.png')
        self.stop_icon_path = get_icon('Stop.png')
        self.movement_icon_path = get_icon('mouse.png')
        self.click_icon_path = get_icon('click.png')
        
        # Crear la lógica del contador (antes de setup_ui para poder conectar señales)
        self.contador_logic = ContadorLogic(self)
        
        self.setup_ui()
        self.apply_styles()
        
        # Conectar la señal del contador a la UI
        self.contador_logic.time_changed.connect(self.counter_display.setText)
        
        # Añadir botón de ayuda con posición absoluta
        self.help_button = HelpButton(self)
        # Posicionar en la esquina superior derecha (16px de margen)
        self.help_button.setGeometry(self.width() - 40, 16, 24, 24)
        self.help_button.clicked.connect(self.show_help)

    def apply_styles(self):
        # Aplicar estilos desde el módulo de estilos
        self.setStyleSheet(get_app_styles())

    def setup_ui(self):
        # Main layout (vertical) que contendrá todo
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)
        
        # Widget contenedor principal (con margen)
        self.main_container = QWidget()
        self.main_layout = QVBoxLayout(self.main_container)
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
        
        # Contador como una barra en la parte inferior de la ventana
        self.counter_widget = QWidget()
        self.counter_widget.setFixedHeight(22)  # Altura del contador
        self.counter_widget.setObjectName("counterWidget")
        
        # Usar un layout absoluto para posicionar directamente los elementos
        self.counter_widget.setLayout(QHBoxLayout())
        self.counter_widget.layout().setContentsMargins(8, 0, 8, 0)
        self.counter_widget.layout().setSpacing(0)
        
        # Icono a la izquierda directamente sobre el fondo
        self.counter_icon = QLabel(self.counter_widget)
        self.counter_icon.setFixedSize(16, 16)
        self.counter_icon.move(8, 3)  # Posición manual
        
        # Establecer icono inicial
        icon = QPixmap(self.movement_icon_path)
        self.counter_icon.setPixmap(icon.scaled(
            16, 16, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        ))
        
        # Etiqueta del contador directamente sobre el fondo a la derecha
        self.counter_display = QLabel("00:00:00", self.counter_widget)
        self.counter_display.setObjectName("counterDisplay")
        self.counter_display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.counter_display.setFont(QFont("Consolas", 10))
        self.counter_display.setGeometry(self.counter_widget.width() - 80, 0, 72, 22)  # Posicionamiento manual
        
        # Ajustar la posición del contador cuando se redimensione
        self.counter_widget.resizeEvent = lambda e: self.counter_display.setGeometry(
            self.counter_widget.width() - 80, 0, 72, 22
        )
        
        # Estilos sin contenedores adicionales
        self.counter_widget.setStyleSheet("""
            #counterWidget {
                background-color: #1e1e1e;
                border-top: 1px solid #333;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 11px;
                border: none;
                padding: 0px;
                margin: 0px;
                background: transparent;
            }
            #counterDisplay {
                color: #D0BCFF;
                font-weight: bold;
                font-family: 'Consolas', 'Courier New', monospace;
                border: none;
                padding: 0px;
                margin: 0px;
                background: transparent;
            }
        """)
        
        # Añadir todo al layout principal externo
        self.outer_layout.addWidget(self.main_container)
        self.outer_layout.addWidget(self.counter_widget)

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
    
    def set_counter_type(self, type_name):
        """Establece qué tipo de operación está activa para mostrar el icono correcto"""
        # Usar la lógica del contador para establecer el tipo
        type_name = self.contador_logic.set_active_type(type_name)
        
        # Cambiar el icono según el tipo activo
        if type_name == "movement":
            icon = QPixmap(self.movement_icon_path)
        else:  # click
            icon = QPixmap(self.click_icon_path)
        
        # Escalar y establecer el icono
        self.counter_icon.setPixmap(icon.scaled(
            16, 16, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        ))
    
    def handle_position_selection_complete(self):
        """Handle completion of position selection"""
        # Position has been selected, now we can start auto-clicking
        settings = self.click_tab.get_current_settings()
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
        
        # Change state and update UI
        self.is_moving = True
        self.position_selection_pending = False
        self.main_button.setIcon(QIcon(self.stop_icon_path))
        self.shortcut_label.setText("Ctrl+Space to stop")
        
        # Iniciar contador con el tipo "click"
        self.set_counter_type("click")
        self.contador_logic.reset_counter()
        self.contador_logic.start_counter()

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
                
                # Change to STOP icon
                self.main_button.setIcon(QIcon(self.stop_icon_path))
                # Update shortcut text
                self.shortcut_label.setText("Ctrl+Space to stop")
                # Change state
                self.is_moving = True
                
                # Iniciar contador con el tipo "movement"
                self.set_counter_type("movement")
                self.contador_logic.reset_counter()
                self.contador_logic.start_counter()
            
            else:  # Click tab
                # Get current settings from click tab
                settings = self.click_tab.get_current_settings()
                
                # Check if we need to select a position first
                # Always prompt for position selection if in "select" mode, regardless of whether we have a previous position
                if settings['position'] == 'select' or (settings['position'] == 'specific' and settings['specific_position'] is None):
                    # Mark that we have a pending position selection
                    self.position_selection_pending = True
                    
                    # Show position selector
                    self.click_tab.show_position_selector()
                    
                    # Connect the position selected signal to continue with auto-click
                    self.click_tab.overlay.positionSelected.connect(lambda: self.handle_position_selection_complete())
                    
                    # Don't change state yet - wait for position selection
                    return
                
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
                # Change state
                self.is_moving = True
                
                # Iniciar contador con el tipo "click"
                self.set_counter_type("click")
                self.contador_logic.reset_counter()
                self.contador_logic.start_counter()
            
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
                
                # Reset the selected position in the click tab if using "Select" mode
                if self.click_tab.position_group.checkedId() == 2:  # If "Select" is checked
                    self.click_tab.selected_position = None
                
                # Log in console
                if self.dev_mode:
                    self.console.log("Auto-click stopped.")
            
            # Change to PLAY icon
            self.main_button.setIcon(QIcon(self.play_icon_path))
            # Update shortcut text
            self.shortcut_label.setText("Ctrl+Space to start")
            # Change state
            self.is_moving = False
            
            # Detener el contador
            self.contador_logic.stop_counter()