"""
Generate a simple icon for SnapStack.
This script creates a basic icon when real assets aren't available.
"""

from PySide6.QtGui import QPainter, QPixmap, QColor, QPen, QBrush, QGuiApplication, QLinearGradient
from PySide6.QtCore import Qt, QRect
import sys

def generate_icon(size=256, app=None):
    """
    Generate a simple icon for SnapStack.
    
    Args:
        size: Size of the icon in pixels
        app: Optional QApplication instance
    
    Returns:
        QPixmap: The generated icon
    """
    # Create a QGuiApplication if one doesn't exist
    local_app = None
    if app is None and not QGuiApplication.instance():
        local_app = QGuiApplication(sys.argv)
    
    # Create a blank pixmap
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    # Create a painter
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Background gradient
    gradient = QLinearGradient(0, 0, size, size)
    gradient.setColorAt(0, QColor(41, 128, 185))  # Blue
    gradient.setColorAt(1, QColor(52, 152, 219))  # Lighter blue
    
    # Draw background
    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(gradient))
    painter.drawRoundedRect(0, 0, size, size, size/10, size/10)
    
    # Draw top and bottom rectangles to represent snapped windows
    # Top window
    painter.setBrush(QColor(236, 240, 241, 230))  # Light gray
    painter.setPen(QPen(QColor(189, 195, 199), size/40))
    top_rect = QRect(size/6, size/6, size*2/3, size/3)
    painter.drawRoundedRect(top_rect, size/30, size/30)
    
    # Bottom window
    painter.setBrush(QColor(236, 240, 241, 230))  # Light gray
    bottom_rect = QRect(size/6, size/2, size*2/3, size/3)
    painter.drawRoundedRect(bottom_rect, size/30, size/30)
    
    # Draw arrow symbols on each window
    painter.setPen(QPen(QColor(41, 128, 185), size/40, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    
    # Up arrow in top window
    arrow_width = size/8
    arrow_height = size/8
    arrow_x = size/2 - arrow_width/2
    
    # Top arrow
    top_arrow_y = size/4
    painter.drawLine(arrow_x, top_arrow_y + arrow_height/2, 
                    arrow_x + arrow_width/2, top_arrow_y)
    painter.drawLine(arrow_x + arrow_width/2, top_arrow_y, 
                    arrow_x + arrow_width, top_arrow_y + arrow_height/2)
    
    # Bottom arrow
    bottom_arrow_y = size*5/8
    painter.drawLine(arrow_x, bottom_arrow_y, 
                    arrow_x + arrow_width/2, bottom_arrow_y + arrow_height/2)
    painter.drawLine(arrow_x + arrow_width/2, bottom_arrow_y + arrow_height/2, 
                    arrow_x + arrow_width, bottom_arrow_y)
    
    # End painting
    painter.end()
    
    # Clean up the local app if we created one
    # Note: We don't call exec() so it's just for initialization
    if local_app:
        del local_app
    
    return pixmap

def save_icon(size=256, filename="assets/icon.png"):
    """
    Generate and save the icon to a file.
    
    Args:
        size: Size of the icon in pixels
        filename: Output filename
    """
    app = QGuiApplication.instance() or QGuiApplication(sys.argv)
    pixmap = generate_icon(size, app)
    success = pixmap.save(filename)
    if success:
        print(f"Successfully saved icon to {filename}")
    else:
        print(f"Failed to save icon to {filename}")
    return success

if __name__ == "__main__":
    # Initialize application
    app = QGuiApplication(sys.argv)
    
    # Generate icons in multiple sizes
    save_icon(256, "assets/icon.png")
    save_icon(64, "assets/icon_small.png")
    save_icon(512, "assets/logo.png")
    
    print("Icons generated successfully!") 