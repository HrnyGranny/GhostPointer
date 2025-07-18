import threading
import random
import time
import logging
import pyautogui

# Disable pyautogui safety feature
pyautogui.FAILSAFE = False

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

drifting = False
thread = None
speed_factor = 25  # Default speed (1-100, higher is faster)
delay_between_moves = 1.0  # Default delay in seconds
stop_on_move = False  # Flag to stop when user moves mouse manually

# Variables para detectar movimiento manual
expected_position = None
manual_movement_detected = False  # Flag para indicar que se detectó movimiento manual

# Variables para el área de movimiento
movement_area_mode = "fullscreen"  # "fullscreen" o "sized"
movement_area = None  # (x, y, width, height) para modo "sized"
pyautogui_movement_area = None  # Nueva variable para las coordenadas de PyAutoGUI

def check_manual_movement():
    """Verifica si se ha detectado movimiento manual"""
    global manual_movement_detected
    result = manual_movement_detected
    manual_movement_detected = False  # Resetear después de consultar
    return result

def _mouse_loop():
    """Main function to move the mouse"""
    global drifting, speed_factor, delay_between_moves, stop_on_move
    global expected_position, manual_movement_detected
    global movement_area_mode, movement_area, pyautogui_movement_area
    
    # Get screen size for fullscreen mode
    screen_width, screen_height = pyautogui.size()
    logging.info(f"Screen size: {screen_width}x{screen_height}")
    
    # Safety margin to avoid edges
    margin = 50
    
    # Logging para verificar el área
    if movement_area_mode == "sized" and pyautogui_movement_area:
        logging.info(f"Using PyAutoGUI movement area: {pyautogui_movement_area}")
    
    while drifting:
        try:
            # Verificar si debemos detectar movimiento manual
            if stop_on_move and expected_position is not None:
                current_position = pyautogui.position()
                # Si la posición actual difiere significativamente de la esperada
                if abs(current_position[0] - expected_position[0]) > 10 or \
                   abs(current_position[1] - expected_position[1]) > 10:
                    # Detectamos movimiento manual
                    logging.info(f"Manual movement detected! Stopping mouse movement.")
                    
                    # Establecer la bandera de movimiento manual
                    manual_movement_detected = True
                    
                    # Detener el movimiento automático
                    drifting = False
                    return
            
            # Current position
            current_x, current_y = pyautogui.position()
            
            # New random position based on movement area mode
            if movement_area_mode == "fullscreen":
                # Full screen movement with margin
                target_x = random.randint(margin, screen_width - margin)
                target_y = random.randint(margin, screen_height - margin)
            else:  # "sized" mode
                if pyautogui_movement_area:
                    # Movement within the defined area using PyAutoGUI coordinates
                    x, y, width, height = pyautogui_movement_area
                    # Apply a smaller margin for the defined area
                    area_margin = min(10, width // 10, height // 10)
                    
                    # Asegurarnos de que no excedemos los límites
                    min_x = max(0, x + area_margin)
                    max_x = min(screen_width, x + width - area_margin)
                    min_y = max(0, y + area_margin)
                    max_y = min(screen_height, y + height - area_margin)
                    
                    # Comprobar que tenemos un rango válido
                    if min_x >= max_x or min_y >= max_y:
                        # Área inválida, usar pantalla completa como respaldo
                        target_x = random.randint(margin, screen_width - margin)
                        target_y = random.randint(margin, screen_height - margin)
                        logging.warning("Invalid area ranges, using fullscreen")
                    else:
                        # Generar objetivo dentro del área
                        target_x = random.randint(min_x, max_x)
                        target_y = random.randint(min_y, max_y)
                        
                    # Logging para depuración
                    logging.debug(f"Target position: ({target_x}, {target_y})")
                else:
                    # Fallback to full screen if no area defined
                    target_x = random.randint(margin, screen_width - margin)
                    target_y = random.randint(margin, screen_height - margin)
            
            # Calculate move duration based on speed factor
            # Higher speed_factor = shorter duration = faster movement
            duration = max(0.1, 2.0 - (speed_factor / 50))  # Scale to reasonable range
            
            # Move the mouse with pyautogui (smooth movement)
            pyautogui.moveTo(target_x, target_y, duration=duration, tween=pyautogui.easeInOutQuad)
            
            # Guardar la posición esperada después del movimiento
            expected_position = (target_x, target_y)
            
            # Wait for the specified delay between movements
            time.sleep(delay_between_moves)
            
        except Exception as e:
            logging.error(f"Error moving mouse: {e}")
            time.sleep(1)  # Wait a bit before retrying

def start_mouse_drift(speed=None, delay=None, stop_on_move_param=False, area=None):
    """Start random mouse movement with specified parameters"""
    global drifting, thread, speed_factor, delay_between_moves, stop_on_move
    global expected_position, manual_movement_detected, movement_area
    
    # Update parameters if provided
    if speed is not None:
        speed_factor = speed
    if delay is not None:
        delay_between_moves = delay  # Ahora ya está en segundos, no necesita conversión
    if area is not None:
        movement_area = area
    
    # Set stop_on_move flag
    stop_on_move = stop_on_move_param
    expected_position = None
    manual_movement_detected = False
    
    if drifting:
        return thread  # Already moving
    
    area_info = f", area={movement_area}" if movement_area_mode == "sized" and movement_area else ""
    
    logging.info(f"Starting mouse movement with speed={speed_factor}, "
                f"delay={delay_between_moves}s, stop_on_move={stop_on_move}, "
                f"mode={movement_area_mode}{area_info}")
    
    drifting = True
    thread = threading.Thread(target=_mouse_loop, daemon=True)
    thread.start()
    return thread

def stop_mouse_drift():
    """Stop random mouse movement"""
    global drifting, movement_area, pyautogui_movement_area
    
    logging.info("Stopping mouse movement")
    drifting = False
    
    # Resete the area
    if movement_area_mode == "sized":
        movement_area = None
        pyautogui_movement_area = None
        logging.info("Movement area has been reset for next selection")

def update_speed(new_speed):
    """Update the speed factor while running"""
    global speed_factor
    speed_factor = new_speed
    logging.info(f"Speed updated to {speed_factor}")

def update_delay(new_delay_seconds):
    """Update the delay between moves while running"""
    global delay_between_moves
    delay_between_moves = new_delay_seconds  # Ya está en segundos, no necesita conversión
    logging.info(f"Delay updated to {delay_between_moves}s")

def update_area_mode(mode):
    """Update the movement area mode"""
    global movement_area_mode
    if mode in ["fullscreen", "sized"]:
        movement_area_mode = mode
        logging.info(f"Movement area mode updated to {movement_area_mode}")

def set_movement_area(x, y, width, height, start_point_pyautogui=None, end_point_pyautogui=None):
    """Set the movement area for sized mode"""
    global movement_area, pyautogui_movement_area
    
    # Guardar las coordenadas Qt originales
    movement_area = (x, y, width, height)
    logging.info(f"Qt movement area set to {movement_area}")
    
    # Si tenemos las coordenadas de PyAutoGUI, usarlas directamente
    if start_point_pyautogui and end_point_pyautogui:
        # Calcular área basada en las coordenadas reales de PyAutoGUI
        pg_x1, pg_y1 = start_point_pyautogui
        pg_x2, pg_y2 = end_point_pyautogui
        
        # Normalizar (asegurarse que el rectángulo tenga anchura y altura positivas)
        pg_left = min(pg_x1, pg_x2)
        pg_top = min(pg_y1, pg_y2)
        pg_width = abs(pg_x2 - pg_x1)
        pg_height = abs(pg_y2 - pg_y1)
        
        # Establecer el área de PyAutoGUI
        pyautogui_movement_area = (pg_left, pg_top, pg_width, pg_height)
        logging.info(f"PyAutoGUI movement area set to {pyautogui_movement_area}")
    else:
        # Si no tenemos coordenadas de PyAutoGUI, usar las de PyAutoGUI actuales
        current_pos = pyautogui.position()
        # Usamos el punto actual como punto final de selección y estimamos el inicio
        pg_x2, pg_y2 = current_pos
        pg_width = width
        pg_height = height
        pg_x1 = pg_x2 - pg_width
        pg_y1 = pg_y2 - pg_height
        
        pyautogui_movement_area = (pg_x1, pg_y1, pg_width, pg_height)
        logging.info(f"Estimated PyAutoGUI area from current position: {pyautogui_movement_area}")

def needs_area_selection():
    """Check if area selection is needed"""
    return movement_area_mode == "sized" and movement_area is None