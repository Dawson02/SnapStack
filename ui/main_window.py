"""
Main window UI for SnapStack application.
Provides the primary interface for the application.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, 
    QLabel, QHBoxLayout, QSystemTrayIcon, QMenu
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QAction
import os.path

# Import icon generator if available
try:
    from assets.icon import generate_icon
    has_icon_generator = True
except ImportError:
    has_icon_generator = False

class MainWindow(QMainWindow):
    """Main application window for SnapStack."""
    
    def __init__(self, snapper, parent=None):
        """Initialize the main window."""
        super(MainWindow, self).__init__(parent)
        
        self.snapper = snapper
        self.setWindowTitle("SnapStack")
        self.setMinimumSize(300, 200)
        
        # Set application icon
        self.app_icon = self.get_application_icon()
        if self.app_icon:
            self.setWindowIcon(self.app_icon)
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Add title label
        self.title_label = QLabel("SnapStack")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        self.layout.addWidget(self.title_label)
        
        # Add description
        self.desc_label = QLabel(
            "Snap windows to the top or bottom half of your screen with keyboard shortcuts."
        )
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setWordWrap(True)
        self.layout.addWidget(self.desc_label)
        
        # Shortcut info
        self.shortcuts_label = QLabel(
            "<b>Keyboard Shortcuts:</b><br>"
            "• Ctrl + Alt + Up: Snap to top half<br>"
            "• Ctrl + Alt + Down: Snap to bottom half"
        )
        self.shortcuts_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.shortcuts_label)
        
        # Button layout
        self.button_layout = QHBoxLayout()
        
        # Add snap buttons
        self.snap_top_button = QPushButton("Snap to Top")
        self.snap_top_button.clicked.connect(self.on_snap_top)
        self.button_layout.addWidget(self.snap_top_button)
        
        self.snap_bottom_button = QPushButton("Snap to Bottom")
        self.snap_bottom_button.clicked.connect(self.on_snap_bottom)
        self.button_layout.addWidget(self.snap_bottom_button)
        
        self.layout.addLayout(self.button_layout)
        
        # Status indicator
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)
        
        # Setup system tray
        self.setup_tray()
    
    def get_application_icon(self):
        """Get the application icon from file or generate one."""
        # Try to load icon from assets
        icon_path = "assets/icon.png"
        small_icon_path = "assets/icon_small.png"
        
        # Check if the icon files exist
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        
        # If the icon generator is available, generate an icon
        if has_icon_generator:
            try:
                # Generate an icon using the provided module
                pixmap = generate_icon(256)
                icon = QIcon(pixmap)
                
                # Save the generated icon for future use
                pixmap.save(icon_path)
                
                # Also generate a small icon for the system tray
                small_pixmap = generate_icon(64)
                small_pixmap.save(small_icon_path)
                
                return icon
            except Exception as e:
                print(f"Failed to generate icon: {e}")
        
        return QIcon()  # Return an empty icon if we couldn't load or generate one
    
    def setup_tray(self):
        """Setup the system tray icon and menu."""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Set the tray icon
        if self.app_icon:
            self.tray_icon.setIcon(self.app_icon)
        
        # Create the tray menu
        tray_menu = QMenu()
        
        # Add actions
        snap_top_action = QAction("Snap to Top", self)
        snap_top_action.triggered.connect(self.on_snap_top)
        tray_menu.addAction(snap_top_action)
        
        snap_bottom_action = QAction("Snap to Bottom", self)
        snap_bottom_action.triggered.connect(self.on_snap_bottom)
        tray_menu.addAction(snap_bottom_action)
        
        tray_menu.addSeparator()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)
        
        # Set the menu
        self.tray_icon.setContextMenu(tray_menu)
        
        # Enable the tray icon
        self.tray_icon.show()
    
    def on_snap_top(self):
        """Handle snap to top button click."""
        result = self.snapper.snap_to_top()
        self.update_status(result, "top")
    
    def on_snap_bottom(self):
        """Handle snap to bottom button click."""
        result = self.snapper.snap_to_bottom()
        self.update_status(result, "bottom")
    
    def update_status(self, success, position):
        """Update the status label based on operation success."""
        if success:
            self.status_label.setText(f"Window snapped to {position}")
        else:
            self.status_label.setText(f"Failed to snap window to {position}")
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Clean up the tray icon
        if self.tray_icon:
            self.tray_icon.hide()
        
        # Accept the close event
        event.accept() 