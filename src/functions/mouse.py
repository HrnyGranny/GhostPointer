import threading
import random
import time
import logging
import pyautogui
from pynput import mouse

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
last_manual_move_time = 0  # Timestamp of last manual mouse movement

# Mouse listener
mouse_listener = None

def on_mouse_move(x, y):
    """Callback function for manual mouse movement detection"""
    global last_manual_move_time
    last_manual_move_time = time.time()
    logging.debug(f"Manual mouse movement detected at {x}, {y}")

def init_mouse_listener():
    """Initialize the mouse listener if needed"""
    global mouse_listener
    if mouse_listener is None:
        mouse_listener = mouse.Listener(on_move=on_mouse_move)
        mouse_listener.daemon = True

def _mouse_loop():
    """Main function to move the mouse"""
    global drifting, speed_factor, delay_between_moves, stop_on_move, last_manual_move_time
    
    # Start mouse listener if stop_on_move is enabled
    if stop_on_move:
        init_mouse_listener()
        if not mouse_listener.running:
            mouse_listener.start()
            logging.info("Mouse movement detection started")
    
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    logging.info(f"Screen size: {screen_width}x{screen_height}")
    
    # Safety margin to avoid edges
    margin = 50
    
    while drifting:
        try:
            # Check if we should pause due to manual movement
            if stop_on_move and (time.time() - last_manual_move_time < 0.5):
                # User moved the mouse manually in the last 0.5 seconds
                # Wait a bit and continue checking
                time.sleep(0.1)
                continue
                
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

def start_mouse_drift(speed=None, delay=None, stop_on_move_param=False):
    """Start random mouse movement with specified parameters"""
    global drifting, thread, speed_factor, delay_between_moves, last_manual_move_time, stop_on_move
    
    # Update parameters if provided
    if speed is not None:
        speed_factor = speed
    if delay is not None:
        delay_between_moves = delay / 1000.0  # Convert from ms to seconds
    
    # Set stop_on_move flag with different parameter name to avoid confusion
    stop_on_move = stop_on_move_param
    last_manual_move_time = time.time()
    
    if drifting:
        return thread  # Already moving
    
    logging.info(f"Starting mouse movement with speed={speed_factor}, delay={delay_between_moves}s, stop_on_move={stop_on_move}")
    drifting = True
    thread = threading.Thread(target=_mouse_loop, daemon=True)
    thread.start()
    return thread

def stop_mouse_drift():
    """Stop random mouse movement"""
    global drifting, mouse_listener
    
    logging.info("Stopping mouse movement")
    drifting = False
    
    # Stop mouse listener if running
    if mouse_listener and mouse_listener.running:
        mouse_listener.stop()
        logging.info("Mouse movement detection stopped")

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