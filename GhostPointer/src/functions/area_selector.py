from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QRect
import pyautogui  # Añadimos esta importación

class AreaSelectorOverlay(QWidget):
    """Overlay transparente para seleccionar un área rectangular en la pantalla"""
    
    # Señal que se emite cuando se selecciona un área
    # Modificamos para enviar también las coordenadas de PyAutoGUI
    areaSelected = pyqtSignal(QRect, tuple, tuple)
    selectionCanceled = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_point = None
        self.current_point = None
        self.is_selecting = False
        self.start_point_pyautogui = None  # Nueva variable para almacenar coordenadas de PyAutoGUI
        
    def initUI(self):
        # Configurar la ventana para que cubra toda la pantalla
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                           Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Obtener el tamaño de la pantalla principal
        screen_rect = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_rect)
        
        # Instrucciones
        self.instruction_label = QLabel("Click and drag to select area\nESC to cancel", self)
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
        """Dibuja el overlay semitransparente con el área seleccionada"""
        painter = QPainter(self)
        
        # Fondo semitransparente
        painter.fillRect(self.rect(), QColor(255, 255, 255, 80))
        
        # Si hay una selección en progreso, dibujar el rectángulo
        if self.start_point and self.current_point:
            # Crear rectángulo a partir de los puntos
            selection_rect = self.get_selection_rect()
            
            # Dibujar área seleccionada con borde azul
            pen = QPen(QColor(0, 120, 215), 2)
            painter.setPen(pen)
            
            # Dibujar rectángulo con relleno transparente
            painter.setBrush(QColor(0, 120, 215, 40))
            painter.drawRect(selection_rect)
            
            # Mostrar dimensiones
            painter.setFont(QFont('Arial', 10))
            width = abs(selection_rect.width())
            height = abs(selection_rect.height())
            text = f"{width} x {height}"
            
            # Posición del texto (arriba del rectángulo)
            text_x = selection_rect.x() + 5
            text_y = selection_rect.y() - 5
            
            # Fondo para el texto
            text_rect = painter.fontMetrics().boundingRect(text)
            text_rect.moveTopLeft(QPoint(text_x, text_y - text_rect.height()))
            text_rect.adjust(-5, -5, 5, 5)
            painter.fillRect(text_rect, QColor(0, 0, 0, 150))
            
            # Dibujar texto
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(text_x, text_y - 5, text)
            
    def get_selection_rect(self):
        """Obtiene el rectángulo normalizado desde los puntos de inicio y fin"""
        if not self.start_point or not self.current_point:
            return QRect()
            
        # Crear rectángulo que va desde el punto inicial al punto actual
        x1, y1 = self.start_point.x(), self.start_point.y()
        x2, y2 = self.current_point.x(), self.current_point.y()
        
        # Normalizar (asegurarse que el rectángulo tenga anchura y altura positivas)
        return QRect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
            
    def mousePressEvent(self, event):
        """Inicia la selección de área"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.pos()
            self.current_point = event.pos()
            self.is_selecting = True
            # Capturar posición PyAutoGUI al inicio
            self.start_point_pyautogui = pyautogui.position()
            self.update()
            
    def mouseMoveEvent(self, event):
        """Actualiza el área mientras se arrastra"""
        if self.is_selecting:
            self.current_point = event.pos()
            self.update()
            
    def mouseReleaseEvent(self, event):
        """Finaliza la selección de área y cierra"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_selecting:
            self.is_selecting = False
            self.current_point = event.pos()
            
            selection_rect = self.get_selection_rect()
            
            # Validar que el área sea lo suficientemente grande
            if selection_rect.width() > 10 and selection_rect.height() > 10:
                # Capturar posición final con PyAutoGUI
                end_point_pyautogui = pyautogui.position()
                
                # Emitir señal con el rectángulo en coordenadas de pantalla
                # Y también las coordenadas PyAutoGUI
                global_rect = QRect(
                    selection_rect.x(), selection_rect.y(),
                    selection_rect.width(), selection_rect.height()
                )
                
                # Enviar tanto el rectángulo de Qt como los puntos de PyAutoGUI
                self.areaSelected.emit(global_rect, self.start_point_pyautogui, end_point_pyautogui)
                self.close()
            
    def keyPressEvent(self, event):
        """Manejar tecla ESC para cancelar"""
        if event.key() == Qt.Key.Key_Escape:
            self.selectionCanceled.emit()
            self.close()