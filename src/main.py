import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from gui.gui import GhostPointerGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Get the absolute path to the assets directory
    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
    app_icon_path = os.path.join(assets_dir, 'GhostPointer.png')
    
    # Set the application icon
    app.setWindowIcon(QIcon(app_icon_path))
    
    window = GhostPointerGUI()
    window.show()
    sys.exit(app.exec())