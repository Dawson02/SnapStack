#!/usr/bin/env python3
"""
SnapStack - Window Management Utility

A lightweight tool for snapping windows to the top or bottom half of the screen.
"""

import sys
import signal
import keyboard
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from snapper import WindowSnapper
from ui.main_window import MainWindow
from utils.monitor_info import get_system_platform, is_supported_platform

class SnapStackApp:
    """Main SnapStack application class."""
    
    def __init__(self):
        """Initialize the SnapStack application."""
        # Create the Qt Application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("SnapStack")
        self.app.setOrganizationName("Dawson Murray")
        
        # Handle Ctrl+C in terminal
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        
        # Create the window snapper
        self.snapper = WindowSnapper()
        
        # Create the main window
        self.main_window = MainWindow(self.snapper)
        
        # Set up global keyboard shortcuts (if supported on platform)
        self.setup_global_shortcuts()
    
    def setup_global_shortcuts(self):
        """Set up global keyboard shortcuts for window snapping."""
        system = get_system_platform()
        
        if system == 'Windows' or system == 'Linux':
            # Direct keyboard library usage for Windows and Linux
            try:
                keyboard.add_hotkey('ctrl+alt+up', self.snapper.snap_to_top)
                keyboard.add_hotkey('ctrl+alt+down', self.snapper.snap_to_bottom)
                print("Global hotkeys registered: Ctrl+Alt+Up/Down")
            except Exception as e:
                print(f"Failed to register global hotkeys: {e}")
        elif system == 'Darwin':
            # For macOS, we'll check periodically if keys are pressed
            # This is a workaround, in a real app, use a native macOS solution
            self.key_timer = QTimer()
            self.key_timer.setInterval(100)  # check every 100ms
            self.key_timer.timeout.connect(self.check_mac_hotkeys)
            self.key_timer.start()
            print("Mac hotkey checker started")
    
    def check_mac_hotkeys(self):
        """Check for hotkey combinations on macOS."""
        try:
            # This is not ideal for production use
            # A better solution would use macOS frameworks like Carbon
            is_ctrl = keyboard.is_pressed('ctrl')
            is_alt = keyboard.is_pressed('alt')
            
            if is_ctrl and is_alt:
                if keyboard.is_pressed('up'):
                    self.snapper.snap_to_top()
                elif keyboard.is_pressed('down'):
                    self.snapper.snap_to_bottom()
        except Exception as e:
            print(f"Error checking Mac hotkeys: {e}")
    
    def run(self):
        """Run the application."""
        # Show the main window
        self.main_window.show()
        
        # Start the event loop
        return self.app.exec()

def main():
    """Application entry point."""
    # Check if platform is supported
    if not is_supported_platform():
        print(f"Platform {get_system_platform()} is not fully supported yet.")
        print("Basic functionality may be limited.")
    
    # Create and run the application
    app = SnapStackApp()
    sys.exit(app.run())

if __name__ == "__main__":
    main() 