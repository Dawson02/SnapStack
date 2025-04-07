"""
Core window snapping functionality for SnapStack.
Handles the logic for capturing and resizing windows to specific screen positions.
"""

import platform
import sys
from utils.monitor_info import get_primary_monitor, get_system_platform

# Import platform-specific modules
system = get_system_platform()

if system == 'Windows':
    import pygetwindow as gw
    from pywinauto import Desktop
elif system == 'Darwin':  # macOS
    # For macOS, we'll need to implement with system-specific commands
    import subprocess
    import re
    import os
elif system == 'Linux':
    # For Linux, implementation will depend on the window manager
    pass
else:
    print(f"Unsupported platform: {system}")
    sys.exit(1)

class WindowSnapper:
    """Main class to handle window snapping operations."""
    
    def __init__(self):
        """Initialize the window snapper."""
        self.monitor = get_primary_monitor()
    
    def get_active_window(self):
        """
        Get the currently active/focused window.
        
        Returns:
            Window object or identifier depending on the platform
        """
        if system == 'Windows':
            try:
                return gw.getActiveWindow()
            except Exception as e:
                print(f"Error getting active window: {e}")
                return None
        elif system == 'Darwin':  # macOS
            try:
                # Get the active window info using AppleScript
                script = '''
                tell application "System Events"
                    set frontApp to name of first application process whose frontmost is true
                    set frontWindow to name of front window of application process frontApp
                    return {frontApp, frontWindow}
                end tell
                '''
                result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
                if result.returncode == 0:
                    app_name, window_name = result.stdout.strip().split(", ")
                    return {"app": app_name, "window": window_name}
                return None
            except Exception as e:
                print(f"Error getting active window: {e}")
                return None
        else:
            # Linux implementation
            return None
    
    def snap_to_top(self):
        """Snap the active window to the top half of the screen."""
        window = self.get_active_window()
        if not window or not self.monitor:
            print("Cannot snap: No active window or monitor information available")
            return False
        
        try:
            if system == 'Windows':
                x = self.monitor.x
                y = self.monitor.y
                width = self.monitor.width
                height = self.monitor.height // 2
                window.moveTo(x, y)
                window.resizeTo(width, height)
            elif system == 'Darwin':  # macOS
                if window:
                    screen_width = subprocess.getoutput("system_profiler SPDisplaysDataType | grep Resolution | awk '{print $2}'")
                    screen_height = subprocess.getoutput("system_profiler SPDisplaysDataType | grep Resolution | awk '{print $4}'")
                    
                    # Convert to integers and calculate top half
                    try:
                        width = int(screen_width)
                        height = int(screen_height) // 2
                        x = 0
                        y = 0
                        
                        # Use AppleScript to position and resize the window
                        script = f'''
                        tell application "{window['app']}"
                            set bounds of front window to {{{x}, {y}, {width}, {height}}}
                        end tell
                        '''
                        subprocess.run(['osascript', '-e', script])
                    except Exception as e:
                        print(f"Error resizing window: {e}")
            
            return True
        except Exception as e:
            print(f"Error snapping window to top: {e}")
            return False
    
    def snap_to_bottom(self):
        """Snap the active window to the bottom half of the screen."""
        window = self.get_active_window()
        if not window or not self.monitor:
            print("Cannot snap: No active window or monitor information available")
            return False
        
        try:
            if system == 'Windows':
                x = self.monitor.x
                y = self.monitor.y + (self.monitor.height // 2)
                width = self.monitor.width
                height = self.monitor.height // 2
                window.moveTo(x, y)
                window.resizeTo(width, height)
            elif system == 'Darwin':  # macOS
                if window:
                    screen_width = subprocess.getoutput("system_profiler SPDisplaysDataType | grep Resolution | awk '{print $2}'")
                    screen_height = subprocess.getoutput("system_profiler SPDisplaysDataType | grep Resolution | awk '{print $4}'")
                    
                    # Convert to integers and calculate bottom half
                    try:
                        width = int(screen_width)
                        height = int(screen_height) // 2
                        x = 0
                        y = height  # Start from the middle of the screen
                        
                        # Use AppleScript to position and resize the window
                        script = f'''
                        tell application "{window['app']}"
                            set bounds of front window to {{{x}, {y}, {width}, {y + height}}}
                        end tell
                        '''
                        subprocess.run(['osascript', '-e', script])
                    except Exception as e:
                        print(f"Error resizing window: {e}")
            
            return True
        except Exception as e:
            print(f"Error snapping window to bottom: {e}")
            return False 