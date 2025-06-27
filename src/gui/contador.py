import time
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

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