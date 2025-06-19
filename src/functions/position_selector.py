from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt, pyqtSignal, QPoint

class PositionSelectorOverlay(QWidget):
    """Overlay transparente para seleccionar una posición en la pantalla"""
    
    # Señal que se emite cuando se selecciona una posición
    positionSelected = pyqtSignal(QPoint)
    selectionCanceled = pyqtSignal()  # Nueva señal para cancelación
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.crosshair_pos = None
        
    def initUI(self):
        # Configurar la ventana para que cubra toda la pantalla
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                           Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Obtener el tamaño de la pantalla principal
        screen_rect = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_rect)
        
        # Instrucciones
        self.instruction_label = QLabel("Haz clic para seleccionar la posición del cursor\nPresiona ESC para cancelar", self)
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 150);
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        """)
        self.instruction_label.adjustSize()
        self.instruction_label.move(
            (self.width() - self.instruction_label.width()) // 2,
            30
        )
        
        # Capturar teclado para ESC
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
    def paintEvent(self, event):
        """Dibuja el overlay semitransparente con retícula"""
        painter = QPainter(self)
        
        # Fondo semitransparente
        painter.fillRect(self.rect(), QColor(255, 255, 255, 80))  # Color blanquecino semitransparente
        
        # Si hay una posición de cursor, dibujar una cruz
        if self.crosshair_pos:
            x, y = self.crosshair_pos.x(), self.crosshair_pos.y()
            
            # Dibujar líneas de mira
            pen = QPen(QColor(0, 120, 215), 2)  # Color azul Windows
            painter.setPen(pen)
            
            # Línea horizontal
            painter.drawLine(0, y, self.width(), y)
            
            # Línea vertical
            painter.drawLine(x, 0, x, self.height())
            
            # Círculo en la intersección
            painter.drawEllipse(x-5, y-5, 10, 10)
            
            # Mostrar coordenadas
            painter.setFont(QFont('Arial', 10))
            text = f"({x}, {y})"
            painter.drawText(x + 15, y - 15, text)
            
    def mouseMoveEvent(self, event):
        """Actualiza la posición del cursor mientras se mueve"""
        self.crosshair_pos = event.pos()
        self.update()  # Redibujar
        
    def mousePressEvent(self, event):
        """Captura la posición seleccionada y cierra"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Emitir la señal con la posición global (convertir float a int)
            pos_x = int(event.globalPosition().x())
            pos_y = int(event.globalPosition().y())
            self.positionSelected.emit(QPoint(pos_x, pos_y))
            self.close()
            
    def keyPressEvent(self, event):
        """Manejar tecla ESC para cancelar"""
        if event.key() == Qt.Key.Key_Escape:
            self.selectionCanceled.emit()  # Emitir señal de cancelación
            self.close()