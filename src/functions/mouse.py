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

def _mouse_loop():
    """Main function to move the mouse"""
    global drifting, speed_factor, delay_between_moves
    
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    logging.info(f"Screen size: {screen_width}x{screen_height}")
    
    # Safety margin to avoid edges
    margin = 50
    
    while drifting:
        try:
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
            
            # Wait for the specified delay between movements
            time.sleep(delay_between_moves)
            
        except Exception as e:
            logging.error(f"Error moving mouse: {e}")
            time.sleep(1)  # Wait a bit before retrying

def start_mouse_drift(speed=None, delay=None):
    """Start random mouse movement with specified parameters"""
    global drifting, thread, speed_factor, delay_between_moves
    
    # Update parameters if provided
    if speed is not None:
        speed_factor = speed
    if delay is not None:
        delay_between_moves = delay / 1000.0  # Convert from ms to seconds
    
    if drifting:
        return thread  # Already moving
    
    logging.info(f"Starting mouse movement with speed={speed_factor}, delay={delay_between_moves}s")
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