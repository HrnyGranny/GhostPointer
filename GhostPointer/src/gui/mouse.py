from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QSlider, QFrame, QButtonGroup,
                             QCheckBox, QSpinBox)
from PyQt6.QtCore import Qt, QRect
from src.functions.mouse import update_speed, update_delay, update_area_mode, set_movement_area
from src.functions.area_selector import AreaSelectorOverlay

class DecimalSpinBox(QSpinBox):
    """SpinBox personalizado que muestra valores con un decimal"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDecimals(1)  # Número de decimales a mostrar
        self.factor = 10     # Factor de multiplicación (10 para un decimal)
        
    def setDecimals(self, decimals):
        self.decimals = decimals
        
    def textFromValue(self, value):
        """Convierte el valor interno a texto con decimal"""
        return f"{value / self.factor:.1f}"
        
    def valueFromText(self, text):
        """Convierte el texto a valor interno"""
        try:
            value = float(text.replace(self.suffix(), "").strip())
            return int(value * self.factor)
        except ValueError:
            return 0
            
    def setValue(self, value):
        """Establece el valor considerando la escala"""
        super().setValue(int(value * self.factor))
            
    def value(self):
        """Devuelve el valor real (con decimales)"""
        return super().value() / self.factor
        
    def setMinimum(self, minimum):
        """Establece el valor mínimo considerando la escala"""
        super().setMinimum(int(minimum * self.factor))
        
    def setMaximum(self, maximum):
        """Establece el valor máximo considerando la escala"""
        super().setMaximum(int(maximum * self.factor))
        
    def setSingleStep(self, step):
        """Establece el paso considerando la escala"""
        super().setSingleStep(int(step * self.factor))

class MouseTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_area = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup for the movement tab with transparent options"""
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 8)  # Reduced bottom margin
        layout.setSpacing(6)  # Reduced spacing
        
        # Button section (FullScreen/Sized)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        # Button group for exclusivity
        self.mode_group = QButtonGroup(self)
        
        fullscreen_btn = QPushButton("FullScreen")
        fullscreen_btn.setObjectName("optionButton")
        fullscreen_btn.setCheckable(True)
        fullscreen_btn.setChecked(True)
        
        sized_btn = QPushButton("Sized")
        sized_btn.setObjectName("optionButton")
        sized_btn.setCheckable(True)
        
        # Add buttons to the group
        self.mode_group.addButton(fullscreen_btn, 1)
        self.mode_group.addButton(sized_btn, 2)
        self.mode_group.setExclusive(True)
        self.mode_group.buttonClicked.connect(self.update_movement_mode)
        
        # Make buttons fill all available width
        button_layout.addWidget(fullscreen_btn, 1)  # 1 indicates proportional space
        button_layout.addWidget(sized_btn, 1)
        
        # Options section with transparent background
        options_frame = QFrame()
        options_frame.setObjectName("transparentFrame")  # Transparent frame
        options_layout = QHBoxLayout(options_frame)  # Changed to HBoxLayout for a single row
        options_layout.setContentsMargins(2, 16, 2, 2)  # Minimal padding
        
        # Delay option with spinbox
        delay_label = QLabel("Delay")
        
        # SpinBox personalizado para valores decimales pero con el estilo de QSpinBox
        self.delay_spinbox = DecimalSpinBox()
        self.delay_spinbox.setMinimum(0.0)        # 0.0 segundos mínimo
        self.delay_spinbox.setMaximum(100.0)      # 100.0 segundos máximo
        self.delay_spinbox.setValue(1.0)          # Default value: 1.0 second
        self.delay_spinbox.setSingleStep(0.1)     # Incrementos de 0.1 segundos
        self.delay_spinbox.setSuffix(" s")        # Sufijo "s" para segundos
        self.delay_spinbox.setFixedWidth(100)
        self.delay_spinbox.valueChanged.connect(self.update_delay_value)
        
        # Create container for Stop label and checkbox
        stop_container = QHBoxLayout()
        
        # Stop label - added to the left of checkbox
        stop_label = QLabel("Stop on move")
        stop_label.setObjectName("stopLabel")
        
        # Checkbox without text
        self.stop_checkbox = QCheckBox("")
        self.stop_checkbox.setChecked(False)
        self.stop_checkbox.setToolTip("Stop automatic movement when you move the mouse manually")
        
        stop_container.addWidget(stop_label)
        stop_container.addWidget(self.stop_checkbox)
        stop_container.setSpacing(2)  # Minimal spacing between label and checkbox
        
        # Add all options to the layout
        options_layout.addWidget(delay_label)
        options_layout.addWidget(self.delay_spinbox)
        options_layout.addStretch(1)  # Stretch to push the stop option to the right
        options_layout.addLayout(stop_container)
        
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
    
    def update_movement_mode(self, button):
        """Update the movement mode based on button selection"""
        button_id = self.mode_group.id(button)
        if button_id == 1:  # FullScreen
            update_area_mode("fullscreen")
            # Reset any previously selected area
            self.selected_area = None
        elif button_id == 2:  # Sized
            update_area_mode("sized")
            # We'll select the area when the user starts the movement
    
    def show_area_selector(self):
        """Muestra el selector de área en pantalla"""
        self.overlay = AreaSelectorOverlay()
        # Conectar con la nueva señal que incluye coordenadas de PyAutoGUI
        self.overlay.areaSelected.connect(self.on_area_selected)
        self.overlay.selectionCanceled.connect(self.on_selection_canceled)
        self.overlay.show()
    
    def on_selection_canceled(self):
        """Maneja la cancelación de la selección de área"""
        # Keep in "Sized" mode, don't switch back to "FullScreen"
        pass
    
    def on_area_selected(self, rect, start_pg=None, end_pg=None):
        """Procesa el área seleccionada"""
        x, y, width, height = rect.x(), rect.y(), rect.width(), rect.height()
        self.selected_area = (x, y, width, height)
        
        print(f"Area selected: ({x}, {y}, {width}, {height})")
        if start_pg and end_pg:
            print(f"PyAutoGUI coords - Start: {start_pg}, End: {end_pg}")
            # Actualizar el área en la lógica del ratón con coordenadas PyAutoGUI
            set_movement_area(x, y, width, height, start_pg, end_pg)
        else:
            # Fallback al método anterior
            set_movement_area(x, y, width, height)
    
    def update_speed_value(self, value):
        """Update the speed value label when slider changes and notify the mouse controller"""
        self.speed_value_label.setText(str(value))
        update_speed(value)
    
    def update_delay_value(self, value):
        """Update the delay between mouse movements"""
        # El valor ya es decimal, lo pasamos directamente
        update_delay(value)
    
    def needs_area_selection(self):
        """Check if area selection is needed"""
        mode_id = self.mode_group.checkedId()
        return mode_id == 2 and self.selected_area is None
    
    def reset_selected_area(self):
        """Resetea el área seleccionada para que se solicite una nueva la próxima vez"""
        self.selected_area = None
    
    def get_current_settings(self):
        """Return current mouse movement settings"""
        return {
            'speed': self.speed_slider.value(),
            'delay': self.delay_spinbox.value(),  # Ya en segundos con decimales
            'stop_on_move': self.stop_checkbox.isChecked(),
            'mode': 'fullscreen' if self.mode_group.checkedId() == 1 else 'sized',
            'area': self.selected_area
        }