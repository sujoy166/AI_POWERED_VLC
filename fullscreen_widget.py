# fullscreen_widget.py - Fullscreen video display widget
import sys
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt


class FullscreenVideoWidget(QWidget):
    """Fullscreen video-only display widget"""
    
    def __init__(self, media_player, parent=None):
        super().__init__(parent)
        self.media_player = media_player
        self.parent_window = parent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: black;")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Enable keyboard focus
        self.showFullScreen()
        self.setFocus()  # Set focus immediately
        
        # Set the video output to this widget
        if sys.platform.startswith('win'):
            self.media_player.set_hwnd(self.winId())
        
        # Create shortcuts for fullscreen mode
        from PyQt6.QtGui import QShortcut, QKeySequence
        
        self.space_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        self.space_shortcut.activated.connect(self.toggle_play_pause)
        
        self.left_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        self.left_shortcut.activated.connect(self.seek_backward)
        
        self.right_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        self.right_shortcut.activated.connect(self.seek_forward)
        
        self.esc_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self.esc_shortcut.activated.connect(self.close)
        
        self.f11_shortcut = QShortcut(QKeySequence(Qt.Key.Key_F11), self)
        self.f11_shortcut.activated.connect(self.close)
        
    def keyPressEvent(self, event):
        """Handle keyboard events in fullscreen mode"""
        if event.key() == Qt.Key.Key_Escape or event.key() == Qt.Key.Key_F11:
            self.close()
        elif event.key() == Qt.Key.Key_Space:
            if self.parent_window:
                self.parent_window.toggle_play_pause()
        elif event.key() == Qt.Key.Key_Left:
            if self.parent_window:
                self.parent_window.seek_backward()
        elif event.key() == Qt.Key.Key_Right:
            if self.parent_window:
                self.parent_window.seek_forward()
        else:
            super().keyPressEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        """Exit fullscreen on double click"""
        self.close()
    
    def toggle_play_pause(self):
        """Toggle play/pause in fullscreen mode"""
        if self.parent_window:
            self.parent_window.toggle_play_pause()
    
    def seek_backward(self):
        """Seek backward in fullscreen mode"""
        if self.parent_window:
            self.parent_window.seek_backward()
            print("Fullscreen: Seeking backward")  # Debug output
    
    def seek_forward(self):
        """Seek forward in fullscreen mode"""
        if self.parent_window:
            self.parent_window.seek_forward()
            print("Fullscreen: Seeking forward")  # Debug output
    
    def closeEvent(self, event):
        """Restore video to main window when closing fullscreen"""
        if self.parent_window:
            self.parent_window.exit_fullscreen()
        event.accept()