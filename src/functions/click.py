import threading
import time
import random
import logging
import pyautogui

# Disable pyautogui safety feature
pyautogui.FAILSAFE = False

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

clicking = False
thread = None
click_interval = 1.0  # Default interval in seconds (1 click per second)
click_type = "left"  # Default click type: "left", "right", "double"
click_position = "current"  # Default position: "current" or "random"
jitter_enabled = False  # Small random movement before clicking
jitter_amount = 5  # Pixels of random jitter

def _click_loop():
    """Main function to perform automatic clicks"""
    global clicking, click_interval, click_type, click_position, jitter_enabled, jitter_amount
    
    # Get screen size for random positions
    screen_width, screen_height = pyautogui.size()
    margin = 50  # Safety margin to avoid edges
    
    while clicking:
        try:
            # If jitter is enabled, add small random movement
            if jitter_enabled:
                current_x, current_y = pyautogui.position()
                jitter_x = random.randint(-jitter_amount, jitter_amount)
                jitter_y = random.randint(-jitter_amount, jitter_amount)
                pyautogui.moveRel(jitter_x, jitter_y, duration=0.1)
            
            # If random position is selected, move to a random screen position
            if click_position == "random":
                target_x = random.randint(margin, screen_width - margin)
                target_y = random.randint(margin, screen_height - margin)
                pyautogui.moveTo(target_x, target_y, duration=0.2)
            
            # Perform the click based on the selected type
            if click_type == "left":
                pyautogui.click()
                logging.debug("Left click performed")
            elif click_type == "right":
                pyautogui.rightClick()
                logging.debug("Right click performed")
            elif click_type == "double":
                pyautogui.doubleClick()
                logging.debug("Double click performed")
            elif click_type == "middle":
                pyautogui.middleClick()
                logging.debug("Middle click performed")
            
            # Wait for the specified interval
            time.sleep(click_interval)
            
        except Exception as e:
            logging.error(f"Error during automatic clicking: {e}")
            time.sleep(1)  # Wait a bit before retrying

def start_auto_click(interval=None, click_method=None, position=None, jitter=None):
    """Start automatic clicking with specified parameters"""
    global clicking, thread, click_interval, click_type, click_position, jitter_enabled
    
    # Update parameters if provided
    if interval is not None:
        click_interval = interval
    if click_method is not None:
        click_type = click_method
    if position is not None:
        click_position = position
    if jitter is not None:
        jitter_enabled = jitter
    
    if clicking:
        return thread  # Already clicking
    
    logging.info(f"Starting auto-click: interval={click_interval}s, type={click_type}, "
                 f"position={click_position}, jitter={jitter_enabled}")
    
    clicking = True
    thread = threading.Thread(target=_click_loop, daemon=True)
    thread.start()
    return thread

def stop_auto_click():
    """Stop automatic clicking"""
    global clicking
    
    logging.info("Stopping auto-click")
    clicking = False

def update_interval(new_interval):
    """Update the interval between clicks while running"""
    global click_interval
    click_interval = new_interval
    logging.info(f"Click interval updated to {click_interval}s")

def update_click_type(new_type):
    """Update the type of click while running"""
    global click_type
    click_type = new_type
    logging.info(f"Click type updated to {click_type}")

def update_position(new_position):
    """Update the click position mode while running"""
    global click_position
    click_position = new_position
    logging.info(f"Click position updated to {click_position}")

def update_jitter(enabled):
    """Enable or disable jitter while running"""
    global jitter_enabled
    jitter_enabled = enabled
    logging.info(f"Jitter {'enabled' if enabled else 'disabled'}")