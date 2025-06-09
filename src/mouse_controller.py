import threading
import random
import time
import logging
import pyautogui

# Desactivar la característica de seguridad de pyautogui
pyautogui.FAILSAFE = False

# Configurar logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

drifting = False
thread = None

def _mouse_loop():
    """Función principal para mover el ratón"""
    global drifting
    
    # Obtener tamaño de pantalla
    screen_width, screen_height = pyautogui.size()
    logging.info(f"Tamaño de pantalla: {screen_width}x{screen_height}")
    
    # Margen de seguridad para no tocar los bordes
    margin = 50
    
    while drifting:
        try:
            # Posición actual
            current_x, current_y = pyautogui.position()
            
            # Nueva posición aleatoria
            target_x = random.randint(margin, screen_width - margin)
            target_y = random.randint(margin, screen_height - margin)
            
            # Duración del movimiento (aleatorio para parecer natural)
            duration = random.uniform(0.5, 1.5)
            
            # Mover el ratón con pyautogui (movimiento suavizado)
            pyautogui.moveTo(target_x, target_y, duration=duration, tween=pyautogui.easeInOutQuad)
            
            # Pausa aleatoria entre movimientos
            time.sleep(random.uniform(1.0, 3.0))
            
        except Exception as e:
            logging.error(f"Error moviendo el ratón: {e}")
            time.sleep(1)  # Esperar un poco antes de reintentar

def start_mouse_drift():
    """Inicia el movimiento aleatorio del ratón"""
    global drifting, thread
    
    if drifting:
        return thread  # Ya está en movimiento
    
    logging.info("Iniciando movimiento del ratón")
    drifting = True
    thread = threading.Thread(target=_mouse_loop, daemon=True)
    thread.start()
    return thread

def stop_mouse_drift():
    """Detiene el movimiento aleatorio del ratón"""
    global drifting
    
    logging.info("Deteniendo movimiento del ratón")
    drifting = False