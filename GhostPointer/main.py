import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from src.gui.gui import GhostPointerGUI
from src.gui.assets import get_icon

if __name__ == "__main__":
    # Esta línea es clave para que el icono aparezca en la barra de tareas de Windows
    myappid = 'hrnygranny.ghostpointer.app.v0.1'  # Identificador único
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass  # Ignorar si no estamos en Windows
    
    app = QApplication(sys.argv)
    
    # Asegúrate de que la ruta al icono es correcta
    app_icon = QIcon(get_icon('GhostPointer.ico'))
    app.setWindowIcon(app_icon)

    window = GhostPointerGUI()
    window.setWindowTitle("GhostPointer v0.1") 
    window.setWindowIcon(app_icon)  # Configurar el icono también en la ventana
    window.show()

    sys.exit(app.exec())