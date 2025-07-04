import threading
import time
import random
import logging
import pyautogui
from datetime import datetime

# Disable pyautogui safety feature
pyautogui.FAILSAFE = False

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Control variables
clicking = False
thread = None
click_interval = 1.0  # Default interval in seconds (1 click per second)
click_type = "left"  # Default click type: "left", "right"
click_position = "current"  # Default position: "current", "select", or "specific"
jitter_enabled = False  # Small random movement before clicking
jitter_amount = 5  # Pixels of random jitter

# Limit variables
click_limit_count = 0  # 0 means no limit (infinite)
click_limit_time = 0  # 0 means no time limit (infinite)
click_counter = 0  # Counter for number of clicks performed
start_time = None  # Start time for time-based limits

# Variables para la posición específica
specific_position = None  # Tupla (x, y) para una posición específica

# Flag to indicate if position selection is needed
position_selection_needed = False

# Add a new variable to store the captured PyAutoGUI position
pyautogui_position = None

def _click_loop():
    """Main function to perform automatic clicks"""
    global clicking, click_interval, click_type, click_position, jitter_enabled, jitter_amount
    global click_limit_count, click_limit_time, click_counter, start_time, pyautogui_position
    
    # Reset counters
    click_counter = 0
    start_time = datetime.now()
    
    # Debug output
    if click_position == "specific" and pyautogui_position:
        print(f"DEBUG - Starting clicking at PyAutoGUI position: {pyautogui_position}")
    
    # Main click loop
    while clicking:
        try:
            # Check for limits
            if click_limit_count > 0 and click_counter >= click_limit_count:
                logging.info(f"Click limit reached: {click_limit_count} clicks")
                stop_auto_click()
                break
                
            if click_limit_time > 0:
                elapsed_seconds = (datetime.now() - start_time).total_seconds()
                if elapsed_seconds >= click_limit_time:
                    logging.info(f"Time limit reached: {click_limit_time} seconds")
                    stop_auto_click()
                    break
            
            # Handle position modes
            if click_position == "specific" and pyautogui_position:
                x, y = pyautogui_position
                
                # Check if we need to move back to the specific position
                current_x, current_y = pyautogui.position()
                distance = ((current_x - x)**2 + (current_y - y)**2)**0.5
                
                # Only move the cursor if it's been significantly moved away from the target
                if distance > 10:  # Only move if more than 10 pixels away
                    # Move cursor back to the target position with animation
                    pyautogui.moveTo(x, y, duration=0.3)
                
                # Apply jitter if enabled
                click_x, click_y = x, y
                if jitter_enabled:
                    jitter_x = random.randint(-jitter_amount, jitter_amount)
                    jitter_y = random.randint(-jitter_amount, jitter_amount)
                    click_x += jitter_x
                    click_y += jitter_y
                    
                    # If jitter is enabled, visually move to the jittered position
                    pyautogui.moveTo(click_x, click_y, duration=0.1)
                
                # Click at the target position (or jittered position)
                if click_type == "left":
                    pyautogui.click()
                else:
                    pyautogui.rightClick()
            
            else:  # current position
                # Apply jitter if enabled
                if jitter_enabled:
                    jitter_x = random.randint(-jitter_amount, jitter_amount)
                    jitter_y = random.randint(-jitter_amount, jitter_amount)
                    pyautogui.moveRel(xOffset=jitter_x, yOffset=jitter_y, duration=0.1)
                
                # Wait for the interval
                time.sleep(click_interval)
                
                # Click at current position
                if click_type == "left":
                    pyautogui.click()
                else:
                    pyautogui.rightClick()
            
            # Increment click counter
            click_counter += 1
            
            
            
        except Exception as e:
            logging.error(f"Error during automatic clicking: {e}")
            print(f"ERROR: {e}")
            time.sleep(1)

def start_auto_click(interval=None, click_method=None, position=None, jitter=None):
    """Start automatic clicking with specified parameters"""
    global clicking, thread, click_interval, click_type, click_position, jitter_enabled
    global position_selection_needed, pyautogui_position
    
    # Update parameters if provided
    if interval is not None:
        click_interval = interval
    if click_method is not None:
        click_type = click_method
    if position is not None:
        click_position = position
    if jitter is not None:
        jitter_enabled = jitter
    
    # Check if we need to select a position first
    if click_position == "select":
        if specific_position is None:
            position_selection_needed = True
            logging.info("Position selection needed before starting auto-click")
            return None
        else:
            # If position was previously selected, use it as specific position
            click_position = "specific"
    
    if clicking:
        return thread  # Already clicking
    
    logging.info(f"Starting auto-click: interval={click_interval}s, type={click_type}, "
                 f"position={click_position}, jitter={jitter_enabled}")
    
    # Log limits if set
    if click_limit_count > 0:
        logging.info(f"Click limit: {click_limit_count} clicks")
    if click_limit_time > 0:
        logging.info(f"Time limit: {click_limit_time} seconds")
    
    clicking = True
    thread = threading.Thread(target=_click_loop, daemon=True)
    thread.start()
    return thread

def stop_auto_click():
    """Stop automatic clicking"""
    global clicking, specific_position, pyautogui_position, position_selection_needed
    
    logging.info("Stopping auto-click")
    clicking = False
    
    # Reset position-related variables when stopping
    # This forces a new position selection next time if "select" mode is active
    if click_position == "select" or click_position == "specific":
        specific_position = None
        pyautogui_position = None
        position_selection_needed = True
        logging.info("Position selection reset for next start")

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
    global click_position, position_selection_needed
    
    click_position = new_position
    
    # If changing to select mode, we'll need to select a position
    # But don't trigger selection yet - just mark that it's needed
    if new_position == "select":
        position_selection_needed = specific_position is None
    
    logging.info(f"Click position updated to {click_position}")

def update_jitter(enabled):
    """Enable or disable jitter while running"""
    global jitter_enabled
    jitter_enabled = enabled
    logging.info(f"Jitter {'enabled' if enabled else 'disabled'}")

def update_delay(milliseconds):
    """Update the delay between clicks in milliseconds"""
    global click_interval
    click_interval = max(milliseconds / 1000.0, 0.050)  # Convert to seconds with min 50ms
    logging.info(f"Click delay updated to {click_interval}s")

def update_limit(clicks, time_sec=0):
    """
    Update the click limit settings
    
    Args:
        clicks: Number of clicks (0 means infinite)
        time_sec: Time limit in seconds (0 means no time limit)
    """
    global click_limit_count, click_limit_time
    
    # Update limits
    click_limit_count = clicks
    click_limit_time = time_sec
    
    # Log the changes
    if clicks > 0:
        logging.info(f"Click limit updated: {clicks} clicks")
    elif time_sec > 0:
        logging.info(f"Time limit updated: {time_sec} seconds")
    else:
        logging.info("Limits removed: infinite clicking")

def set_specific_position(x, y):
    """Establecer una posición específica para los clics"""
    global specific_position, position_selection_needed, pyautogui_position
    
    # Store the QT coordinates (we won't use these directly)
    specific_position = (int(x), int(y))
    position_selection_needed = False
    logging.info(f"QT position establecida: ({x}, {y})")
    
    # IMPORTANT: Get the current mouse position from PyAutoGUI
    # This happens right after the user has clicked in the position selector
    # So the mouse is actually at the correct position already
    pyautogui_position = pyautogui.position()
    logging.info(f"PyAutoGUI position captured: {pyautogui_position}")
    
    print(f"DEBUG - QT position: {specific_position}")
    print(f"DEBUG - PyAutoGUI position: {pyautogui_position}")

def needs_position_selection():
    """Check if position selection is needed"""
    return click_position == "select" and specific_position is None

def reset_position_selection_state():
    """Reset the position selection state after cancellation"""
    global position_selection_needed
    position_selection_needed = False

def is_clicking():
    """Retorna si el auto-click está activo actualmente"""
    global clicking
    return clicking