import sys
import os

def resource_path(relative_path):
    """
    Returns the absolute path to the resource, compatible with PyInstaller and development.
    Looks for resources in the 'assets' folder at the same level as main.py.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller: assets are located inside _MEIPASS/assets/
        return os.path.join(sys._MEIPASS, 'assets', relative_path)
    else:
        # Development: assets are located next to main.py
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        return os.path.join(base_path, 'assets', relative_path)

def get_icon(name):
    return resource_path(name)