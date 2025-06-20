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

def _click_loop():
    """Main function to perform automatic clicks"""
    global clicking, click_interval, click_type, click_position, jitter_enabled, jitter_amount
    global click_limit_count, click_limit_time, click_counter, start_time, specific_position
    
    # Reset counters
    click_counter = 0
    start_time = datetime.now()
    
    # Debug log
    if click_position == "specific" and specific_position:
        print(f"DEBUG - Starting clicking at specific position: {specific_position}")
    
    # Main click loop
    while clicking:
        try:
            # Check for click limit if set
            if click_limit_count > 0 and click_counter >= click_limit_count:
                logging.info(f"Click limit reached: {click_limit_count} clicks")
                stop_auto_click()
                break
                
            # Check for time limit if set
            if click_limit_time > 0:
                elapsed_seconds = (datetime.now() - start_time).total_seconds()
                if elapsed_seconds >= click_limit_time:
                    logging.info(f"Time limit reached: {click_limit_time} seconds")
                    stop_auto_click()
                    break
            
            # Handle different position modes
            if click_position == "specific" and specific_position:
                # Get the exact coordinates from specific_position
                target_x, target_y = specific_position
                
                # Move directly to the specific position (with animation as you prefer)
                pyautogui.moveTo(x=target_x, y=target_y, duration=0.3)
                
                # Apply jitter if enabled (AFTER moving to specific position)
                if jitter_enabled:
                    jitter_x = random.randint(-jitter_amount, jitter_amount)
                    jitter_y = random.randint(-jitter_amount, jitter_amount)
                    # Use moveRel for jitter to ensure it's relative to the specific position
                    pyautogui.moveRel(xOffset=jitter_x, yOffset=jitter_y, duration=0.1)
                
                # Get the final click position (after jitter if applied)
                click_x, click_y = pyautogui.position()
                
                # Perform the click at the CURRENT position
                if click_type == "left":
                    pyautogui.click(x=click_x, y=click_y, button='left')
                else:
                    pyautogui.click(x=click_x, y=click_y, button='right')
            
            else:  # current position mode
                # Get current position
                current_x, current_y = pyautogui.position()
                
                # Apply jitter if enabled
                if jitter_enabled:
                    jitter_x = random.randint(-jitter_amount, jitter_amount)
                    jitter_y = random.randint(-jitter_amount, jitter_amount)
                    pyautogui.moveRel(xOffset=jitter_x, yOffset=jitter_y, duration=0.1)
                
                # Click at current position (after jitter)
                if click_type == "left":
                    pyautogui.click(button='left')
                else:
                    pyautogui.click(button='right')
            
            # Increment click counter
            click_counter += 1
            
            # Wait for the specified interval
            time.sleep(click_interval)
            
        except Exception as e:
            logging.error(f"Error during automatic clicking: {e}")
            print(f"ERROR: {e}")
            time.sleep(1)  # Wait a bit before retrying

def start_auto_click(interval=None, click_method=None, position=None, jitter=None):
    """Start automatic clicking with specified parameters"""
    global clicking, thread, click_interval, click_type, click_position, jitter_enabled
    global position_selection_needed
    
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
    global specific_position, position_selection_needed
    # Ensure we're using exact screen coordinates
    specific_position = (int(x), int(y))
    position_selection_needed = False
    logging.info(f"Posición específica establecida: ({x}, {y})")

def needs_position_selection():
    """Check if position selection is needed"""
    return click_position == "select" and specific_position is None

def reset_position_selection_state():
    """Reset the position selection state after cancellation"""
    global position_selection_needed
    position_selection_needed = False