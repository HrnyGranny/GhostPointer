from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from mouse_controller import start_mouse_drift, stop_mouse_drift

class GhostPointerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("👻 GhostPointer")
        self.setFixedSize(400, 250)
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                background-color: #673AB7;
                padding: 12px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                color: white;
            }
            QPushButton:hover {
                background-color: #5E35B1;
            }
        """)

        self.layout = QVBoxLayout()

        self.title = QLabel("👻 GhostPointer")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))

        self.button = QPushButton("Iniciar movimiento")
        self.button.clicked.connect(self.toggle_movement)

        self.status = QLabel("Estado: detenido")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setFont(QFont("Segoe UI", 12))

        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.status)
        self.layout.addStretch()
        self.setLayout(self.layout)

        self.is_moving = False

    def toggle_movement(self):
        if not self.is_moving:
            start_mouse_drift()
            self.status.setText("Estado: moviendo el ratón...")
            self.button.setText("Detener movimiento")
        else:
            stop_mouse_drift()
            self.status.setText("Estado: detenido")
            self.button.setText("Iniciar movimiento")
        self.is_moving = not self.is_moving