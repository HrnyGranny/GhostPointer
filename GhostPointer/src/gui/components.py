from PyQt6.QtWidgets import (QWidget, QTabWidget, QPushButton, QHBoxLayout, QTextEdit)
from PyQt6.QtGui import (QPainter, QPainterPath, QBrush, QColor, QIcon, QPixmap)
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QSize, QObject, QTimer

import time

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
        self.setObjectName("iconButton")
        # Make the button flat
        self.setFlat(True)


class HelpButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(24, 24)
        self.setText("?")
        self.setObjectName("helpButton")


class ContadorLogic(QObject):
    """
    Clase que maneja la lógica del contador, separada de la interfaz gráfica.
    Emite señales cuando cambia el tiempo para actualizar la UI.
    """
    time_changed = pyqtSignal(str)  # Señal que emite el tiempo formateado
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Estado y variables
        self.start_time = 0
        self.is_running = False
        self.active_type = "movement"  # movement o click
        
        # Configurar timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_counter)
        self.timer.setInterval(100)  # Actualizar cada 100ms para que sea suave
    
    def set_active_type(self, type_name):
        """Establece qué tipo de operación está activa"""
        self.active_type = type_name
        return self.active_type
    
    def start_counter(self):
        """Inicia el contador"""
        self.start_time = time.time()
        self.is_running = True
        self.timer.start()
    
    def stop_counter(self):
        """Detiene el contador"""
        self.is_running = False
        self.timer.stop()
    
    def reset_counter(self):
        """Reinicia el contador a cero"""
        self.time_changed.emit("00:00:00")
    
    def update_counter(self):
        """Actualiza el contador y emite la señal con el tiempo actualizado"""
        if not self.is_running:
            return
        
        # Calcular tiempo transcurrido
        elapsed_time = time.time() - self.start_time
        
        # Formatear tiempo como HH:MM:SS
        hours = int(elapsed_time / 3600)
        minutes = int((elapsed_time % 3600) / 60)
        seconds = int(elapsed_time % 60)
        
        # Emitir señal con el tiempo formateado
        self.time_changed.emit(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

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

    def show_banner(self):
        """Muestra un banner compacto y estilizado en la consola"""
        import datetime
        
        # Obtener fecha actual
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        version = "1.2.0"
        
        # Banner compacto con colores HTML
        banner = f"""<pre style="color:#6750A4; font-family:'Consolas', 'Courier New'">
        ╭────────── <span style="color:#D0BCFF; font-weight:bold">Ghost Pointer</span> ──────────╮
        │ <span style="color:#B0B0B0">v{version}</span>          <span style="color:#B0B0B0">{current_date}</span>  │
        │ <span style="color:#E1E1E1">Developer mode</span>       <span style="color:#B0B0B0">@HrnyGranny</span>  │
        ╰───────────────────────────────────╯</pre>
    """
        
        # Limpiar consola primero
        self.clear()
        
        # Mostrar banner
        self.insertHtml(banner)