import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from src.gui.gui import GhostPointerGUI
from src.gui.assets import get_icon

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_icon('GhostPointer.ico')))  

    window = GhostPointerGUI()
    window.setWindowTitle("GhostPointer v0.1") 
    window.show()

    sys.exit(app.exec())