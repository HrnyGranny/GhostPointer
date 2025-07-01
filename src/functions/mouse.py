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
    
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    logging.info(f"Screen size: {screen_width}x{screen_height}")
    
    # Safety margin to avoid edges
    margin = 50
    
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
            
            # New random position
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

def start_mouse_drift(speed=None, delay=None, stop_on_move_param=False):
    """Start random mouse movement with specified parameters"""
    global drifting, thread, speed_factor, delay_between_moves, stop_on_move
    global expected_position, manual_movement_detected
    
    # Update parameters if provided
    if speed is not None:
        speed_factor = speed
    if delay is not None:
        delay_between_moves = delay / 1000.0  # Convert from ms to seconds
    
    # Set stop_on_move flag
    stop_on_move = stop_on_move_param
    expected_position = None
    manual_movement_detected = False
    
    if drifting:
        return thread  # Already moving
    
    logging.info(f"Starting mouse movement with speed={speed_factor}, delay={delay_between_moves}s, stop_on_move={stop_on_move}")
    drifting = True
    thread = threading.Thread(target=_mouse_loop, daemon=True)
    thread.start()
    return thread

def stop_mouse_drift():
    """Stop random mouse movement"""
    global drifting
    
    logging.info("Stopping mouse movement")
    drifting = False

def update_speed(new_speed):
    """Update the speed factor while running"""
    global speed_factor
    speed_factor = new_speed
    logging.info(f"Speed updated to {speed_factor}")

def update_delay(new_delay_ms):
    """Update the delay between moves while running"""
    global delay_between_moves
    delay_between_moves = new_delay_ms / 1000.0  # Convert from ms to seconds
    logging.info(f"Delay updated to {delay_between_moves}s")