import sys
from PyQt6.QtWidgets import QApplication
from gui import GhostPointerGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GhostPointerGUI()
    window.show()
    sys.exit(app.exec())