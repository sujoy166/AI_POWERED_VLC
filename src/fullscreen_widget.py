# fullscreen_widget.py - Fullscreen video display widget
import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt6.QtGui import QCursor


class FullscreenVideoWidget(QWidget):
    """Fullscreen video-only display widget with auto-hiding controls"""
    
    def __init__(self, media_player, parent=None):
        super().__init__(parent)
        self.media_player = media_player
        self.parent_window = parent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: black;")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.showFullScreen()
        self.setFocus()
        
        # Mouse tracking
        self.setMouseTracking(True)
        self.controls_visible = False
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self.hide_controls)
        self.hide_timer.setSingleShot(True)
        
        # Set the video output to this widget
        if sys.platform.startswith('win'):
            self.media_player.set_hwnd(self.winId())
        
        self.setup_ui()
        self.setup_shortcuts()
    
    def setup_ui(self):
        """Setup the fullscreen UI with controls"""
        from PyQt6.QtWidgets import QFrame
        import sys
        sys.path.insert(0, '../src')
        try:
            import ui_styles
        except:
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
            import ui_styles
        
        # Controls panel at bottom
        self.controls_panel = QWidget(self)
        self.controls_panel.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 rgba(228, 90, 146, 200), 
                                          stop: 1 rgba(209, 71, 127, 200));
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """)
        
        controls_layout = QVBoxLayout(self.controls_panel)
        controls_layout.setContentsMargins(20, 10, 20, 10)
        
        # Progress slider
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setRange(0, 1000)
        self.progress_slider.setStyleSheet(ui_styles.PROGRESS_SLIDER_STYLE)
        controls_layout.addWidget(self.progress_slider)
        
        # Buttons row
        buttons_layout = QHBoxLayout()
        
        self.play_pause_btn = QPushButton("⏸ Pause")
        self.exit_fullscreen_btn = QPushButton("⛶ Exit Fullscreen")
        
        for btn in [self.play_pause_btn, self.exit_fullscreen_btn]:
            btn.setStyleSheet(ui_styles.BUTTON_STYLE + "padding: 10px 20px;")
        
        buttons_layout.addWidget(self.play_pause_btn)
        buttons_layout.addWidget(self.exit_fullscreen_btn)
        buttons_layout.addStretch()
        
        # Timestamp
        self.timestamp_label = QLabel("00:00:00 / 00:00:00")
        self.timestamp_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        buttons_layout.addWidget(self.timestamp_label)
        
        controls_layout.addLayout(buttons_layout)
        
        # Voice command panel - always visible in top-right
        self.voice_panel = QWidget(self)
        self.voice_panel.setStyleSheet("""
            QWidget {
                background: rgba(100, 127, 188, 180);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        voice_layout = QVBoxLayout(self.voice_panel)
        voice_layout.setContentsMargins(10, 10, 10, 10)
        
        self.voice_btn = QPushButton("🎤 Voice Control")
        self.voice_btn.setStyleSheet(ui_styles.BUTTON_STYLE + "font-size: 13px; padding: 8px 15px;")
        voice_layout.addWidget(self.voice_btn)
        
        self.voice_status = QLabel("Standby")
        self.voice_status.setStyleSheet("color: white; font-size: 10px;")
        self.voice_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        voice_layout.addWidget(self.voice_status)
        
        # Connect signals
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        self.exit_fullscreen_btn.clicked.connect(self.close)
        self.voice_btn.clicked.connect(self.trigger_voice_command)
        self.progress_slider.sliderMoved.connect(self.on_slider_moved)
        
        # Position controls panel at bottom (hidden initially)
        self.position_controls()
        self.controls_panel.hide()
        
        # Position voice panel at top-right (always visible)
        self.voice_panel.move(self.width() - 180, 20)
        self.voice_panel.show()
        
        # Update timer for timestamp
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui)
        self.update_timer.start(500)
    
    def setup_shortcuts(self):
        """Create shortcuts for fullscreen mode"""
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
    
    def position_controls(self):
        """Position the controls panel at bottom"""
        panel_height = 120
        self.controls_panel.setGeometry(0, self.height() - panel_height, self.width(), panel_height)
    
    def mouseMoveEvent(self, event):
        """Show/hide controls based on mouse position"""
        pos = event.pos()
        
        # Show controls if mouse is in bottom 150 pixels
        if pos.y() > self.height() - 150:
            self.show_controls()
        else:
            self.hide_timer.start(2000)  # Hide after 2 seconds of no activity
        
        super().mouseMoveEvent(event)
    
    def show_controls(self):
        """Show the controls panel"""
        if not self.controls_visible:
            self.controls_panel.show()
            self.controls_visible = True
        self.hide_timer.stop()
    
    def hide_controls(self):
        """Hide the controls panel"""
        # Only hide if mouse is not over controls
        mouse_pos = self.mapFromGlobal(QCursor.pos())
        if mouse_pos.y() < self.height() - 150:
            self.controls_panel.hide()
            self.controls_visible = False
    
    def resizeEvent(self, event):
        """Reposition controls on window resize"""
        super().resizeEvent(event)
        self.position_controls()
        # Reposition voice panel
        if hasattr(self, 'voice_panel'):
            self.voice_panel.move(self.width() - 180, 20)
    
    def update_ui(self):
        """Update UI elements"""
        if self.media_player and self.media_player.is_playing():
            # Update progress
            position = int(self.media_player.get_position() * 1000)
            self.progress_slider.setValue(position)
            
            # Update timestamp
            current_time = self.media_player.get_time()
            duration = self.media_player.get_length()
            self.timestamp_label.setText(f"{self.format_time(current_time)} / {self.format_time(duration)}")
            
            # Update play/pause button
            self.play_pause_btn.setText("⏸ Pause")
        else:
            self.play_pause_btn.setText("▶ Play")
    
    def format_time(self, milliseconds):
        """Convert milliseconds to HH:MM:SS format"""
        if milliseconds < 0:
            return "00:00:00"
        seconds = milliseconds // 1000
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def on_slider_moved(self, position):
        """Handle slider movement"""
        if self.parent_window:
            self.parent_window.set_position(position)
    
    def trigger_voice_command(self):
        """Trigger voice command from parent window"""
        if self.parent_window and hasattr(self.parent_window, 'start_voice_recording'):
            self.parent_window.start_voice_recording()
            self.voice_status.setText("Listening...")
    
    def keyPressEvent(self, event):
        """Handle keyboard events in fullscreen mode"""
        if event.key() == Qt.Key.Key_Escape or event.key() == Qt.Key.Key_F11:
            self.close()
        elif event.key() == Qt.Key.Key_Space:
            self.toggle_play_pause()
        else:
            super().keyPressEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        """Exit fullscreen on double click"""
        self.close()
    
    def toggle_play_pause(self):
        """Toggle play/pause in fullscreen mode"""
        if self.parent_window:
            self.parent_window.toggle_play_pause()
    
    def closeEvent(self, event):
        """Restore video to main window when closing fullscreen"""
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()
        if self.parent_window:
            self.parent_window.exit_fullscreen()
        event.accept()