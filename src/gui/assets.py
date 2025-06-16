import sys
import os

def resource_path(relative_path):
    """
    Devuelve la ruta absoluta al recurso, compatible con PyInstaller y desarrollo.
    Busca los recursos en la carpeta 'assets' al mismo nivel que main.py.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller: assets queda dentro de _MEIPASS/assets/
        return os.path.join(sys._MEIPASS, 'assets', relative_path)
    else:
        # Desarrollo: assets está al lado de main.py
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        return os.path.join(base_path, 'assets', relative_path)

def get_icon(name):
    return resource_path(name)