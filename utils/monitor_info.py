"""
Monitor information utility module for SnapStack.
Provides functions to get screen dimensions and monitor information.
"""

import platform
from screeninfo import get_monitors

def get_screen_info():
    """
    Get information about all connected monitors.
    
    Returns:
        List of monitor objects containing dimensions and position
    """
    try:
        monitors = get_monitors()
        return monitors
    except Exception as e:
        print(f"Error getting monitor info: {e}")
        return []

def get_primary_monitor():
    """
    Get information about the primary monitor.
    
    Returns:
        Monitor object for the primary display or the first available monitor
    """
    monitors = get_screen_info()
    
    # Try to find primary monitor
    for monitor in monitors:
        if hasattr(monitor, 'is_primary') and monitor.is_primary:
            return monitor
    
    # If no primary monitor is flagged, return the first one
    if monitors:
        return monitors[0]
    
    # Fallback values if no monitor info is available
    return None

def get_system_platform():
    """
    Get the current operating system.
    
    Returns:
        String: 'Windows', 'Darwin' (Mac), or 'Linux'
    """
    return platform.system()

def is_supported_platform():
    """
    Check if the current platform is supported by SnapStack.
    
    Returns:
        Boolean: True if supported, False otherwise
    """
    system = get_system_platform()
    return system in ['Windows', 'Darwin', 'Linux'] 