from PyQt6.QtWidgets import (QWidget, QTabWidget, QPushButton)
from PyQt6.QtGui import (QPainter, QPainterPath, QBrush, QColor, QIcon)
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QSize

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

class HelpButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(24, 24)
        self.setText("?")
        self.setStyleSheet("""
            QPushButton {
                background-color: #31303A;
                color: #D0BCFF;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6750A4;
                color: white;
            }
            QPushButton:pressed {
                background-color: #4F3B8B;
            }
        """)