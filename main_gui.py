# main_gui.py - Main GUI application window
import os
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QSlider, QLabel, 
                            QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut, QAction

# Import our custom modules
from video_player import VideoPlayer
from fullscreen_widget import FullscreenVideoWidget
import ui_styles


class VLCPlayerGUI(QMainWindow):
    """Main GUI window for the AI-VLC Player"""
    
    def __init__(self):
        super().__init__()
        self.video_player = VideoPlayer()
        self.current_file = None
        self.is_fullscreen = False
        self.fullscreen_widget = None
        self.init_ui()
        self.connect_signals()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("AI-VLC Player")
        self.setGeometry(100, 100, 900, 650)
        
        # Set modern window style
        self.setStyleSheet(ui_styles.MAIN_WINDOW_STYLE)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Video display area with modern styling
        self.video_frame = QWidget()
        self.video_frame.setStyleSheet(ui_styles.VIDEO_FRAME_STYLE)
        self.video_frame.setMinimumHeight(420)
        self.video_frame.mouseDoubleClickEvent = self.toggle_fullscreen
        self.video_frame.mousePressEvent = self.video_frame_clicked  # Add click handler to set focus
        main_layout.addWidget(self.video_frame)
        
        # Controls layout
        controls_layout = QVBoxLayout()
        
        # Progress slider with modern styling
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setRange(0, 1000)
        self.progress_slider.sliderMoved.connect(self.set_position)
        self.progress_slider.sliderPressed.connect(self.on_slider_press)
        self.progress_slider.setStyleSheet(ui_styles.PROGRESS_SLIDER_STYLE)
        controls_layout.addWidget(self.progress_slider)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        self.open_btn = QPushButton(ui_styles.BUTTON_TEXTS['open'])
        self.play_btn = QPushButton(ui_styles.BUTTON_TEXTS['play'])
        self.pause_btn = QPushButton(ui_styles.BUTTON_TEXTS['pause'])
        self.stop_btn = QPushButton(ui_styles.BUTTON_TEXTS['stop'])
        
        # Apply button styling
        for btn in [self.open_btn, self.play_btn, self.pause_btn, self.stop_btn]:
            btn.setStyleSheet(ui_styles.BUTTON_STYLE)
        
        # Add tooltips
        self.open_btn.setToolTip(ui_styles.TOOLTIPS['open_btn'])
        self.play_btn.setToolTip(ui_styles.TOOLTIPS['play_btn'])
        self.pause_btn.setToolTip(ui_styles.TOOLTIPS['pause_btn'])
        self.stop_btn.setToolTip(ui_styles.TOOLTIPS['stop_btn'])
        self.progress_slider.setToolTip(ui_styles.TOOLTIPS['progress_slider'])
        
        buttons_layout.addWidget(self.open_btn)
        buttons_layout.addSpacing(10)
        buttons_layout.addWidget(self.play_btn)
        buttons_layout.addWidget(self.pause_btn)
        buttons_layout.addWidget(self.stop_btn)
        buttons_layout.addStretch()
        
        # Volume control with modern styling
        volume_layout = QHBoxLayout()
        volume_label = QLabel("🔊 Volume:")
        volume_label.setStyleSheet(ui_styles.VOLUME_LABEL_STYLE)
        volume_layout.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setMaximumWidth(120)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.volume_slider.setStyleSheet(ui_styles.VOLUME_SLIDER_STYLE)
        self.volume_slider.setToolTip(ui_styles.TOOLTIPS['volume_slider'])
        volume_layout.addWidget(self.volume_slider)
        
        buttons_layout.addLayout(volume_layout)
        controls_layout.addLayout(buttons_layout)
        
        # Status label with modern styling
        self.status_label = QLabel(ui_styles.STATUS_MESSAGES['ready'])
        self.status_label.setStyleSheet(ui_styles.STATUS_LABEL_STYLE)
        controls_layout.addWidget(self.status_label)
        
        main_layout.addLayout(controls_layout)
        
        # Connect video player to video frame
        if sys.platform.startswith('win'):
            self.video_player.media_player.set_hwnd(self.video_frame.winId())
        
    def connect_signals(self):
        """Connect button signals and keyboard shortcuts"""
        self.open_btn.clicked.connect(self.open_file)
        self.play_btn.clicked.connect(self.play_video)
        self.pause_btn.clicked.connect(self.pause_video)
        self.stop_btn.clicked.connect(self.stop_video)
        
        # Connect video player signals
        self.video_player.position_changed.connect(self.update_progress)
        
        # Keyboard shortcuts - ensure proper focus handling
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()  # Set initial focus to main window
        
        # Make video frame focusable for keyboard events
        self.video_frame.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Create global shortcuts that work regardless of focus
        self.space_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        self.space_shortcut.activated.connect(self.toggle_play_pause)
        
        self.left_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        self.left_shortcut.activated.connect(self.seek_backward)
        
        self.right_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        self.right_shortcut.activated.connect(self.seek_forward)
        
        self.f11_shortcut = QShortcut(QKeySequence(Qt.Key.Key_F11), self)
        self.f11_shortcut.activated.connect(self.toggle_fullscreen)
        
        self.esc_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self.esc_shortcut.activated.connect(self.handle_escape)
        
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        if event.key() == Qt.Key.Key_Space:
            self.toggle_play_pause()
        elif event.key() == Qt.Key.Key_Left:
            self.seek_backward()
        elif event.key() == Qt.Key.Key_Right:
            self.seek_forward()
        elif event.key() == Qt.Key.Key_F11:
            self.toggle_fullscreen()
        elif event.key() == Qt.Key.Key_Escape:
            if self.is_fullscreen:
                self.exit_fullscreen()
        else:
            super().keyPressEvent(event)
    
    def open_file(self):
        """Open file dialog to select video"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Video File", 
            "", 
            "Video files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm);;All files (*.*)"
        )
        
        if file_path:
            self.current_file = file_path
            self.status_label.setText(ui_styles.STATUS_MESSAGES['loaded'].format(os.path.basename(file_path)))
            
    def play_video(self):
        """Start playing video"""
        if self.current_file:
            self.video_player.load_video(self.current_file)
            self.status_label.setText(ui_styles.STATUS_MESSAGES['playing'])
        else:
            QMessageBox.warning(self, "Warning", "Please select a video file first!")
            
    def pause_video(self):
        """Pause video playback"""
        self.video_player.pause()
        self.status_label.setText(ui_styles.STATUS_MESSAGES['paused'])
        
    def stop_video(self):
        """Stop video playback"""
        self.video_player.stop()
        self.status_label.setText(ui_styles.STATUS_MESSAGES['stopped'])
        self.progress_slider.setValue(0)
        
    def set_position(self, position):
        """Set video position"""
        self.video_player.set_position(position)
    
    def on_slider_press(self):
        """Handle mouse click on progress slider"""
        position = self.progress_slider.value()
        self.video_player.set_position(position)
        
    def set_volume(self, volume):
        """Set video volume"""
        self.video_player.set_volume(volume)
        
    def update_progress(self, position):
        """Update progress slider"""
        self.progress_slider.setValue(position)
    
    def toggle_play_pause(self):
        """Toggle between play and pause"""
        if self.video_player.media_player.is_playing():
            self.pause_video()
        else:
            if self.current_file:
                # Just resume playing, don't reload the video
                self.video_player.play()
                self.status_label.setText(ui_styles.STATUS_MESSAGES['playing'])
    
    def seek_backward(self):
        """Seek backward by 10 seconds"""
        if self.current_file and self.video_player.media_player.get_length() > 0:
            current_time = self.video_player.media_player.get_time()
            new_time = max(0, current_time - 10000)  # 10 seconds in milliseconds
            self.video_player.media_player.set_time(new_time)
            # Update progress slider
            total_time = self.video_player.media_player.get_length()
            if total_time > 0:
                position = int((new_time / total_time) * 1000)
                self.progress_slider.setValue(position)
            # Show status message
            self.status_label.setText("⏪ Seeking backward 10 seconds")
            print(f"Seeking backward: {current_time} -> {new_time}")  # Debug output
    
    def seek_forward(self):
        """Seek forward by 10 seconds"""
        if self.current_file and self.video_player.media_player.get_length() > 0:
            current_time = self.video_player.media_player.get_time()
            total_time = self.video_player.media_player.get_length()
            new_time = min(total_time, current_time + 10000)  # 10 seconds in milliseconds
            self.video_player.media_player.set_time(new_time)
            # Update progress slider
            if total_time > 0:
                position = int((new_time / total_time) * 1000)
                self.progress_slider.setValue(position)
            # Show status message
            self.status_label.setText("⏩ Seeking forward 10 seconds")
            print(f"Seeking forward: {current_time} -> {new_time}")  # Debug output
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        if not self.current_file:
            self.status_label.setText(ui_styles.STATUS_MESSAGES['load_first'])
            return
            
        if self.is_fullscreen:
            self.exit_fullscreen()
        else:
            self.enter_fullscreen()
    
    def enter_fullscreen(self):
        """Enter fullscreen mode - video only"""
        if not self.is_fullscreen and self.current_file:
            self.is_fullscreen = True
            self.fullscreen_widget = FullscreenVideoWidget(self.video_player.media_player, self)
            self.status_label.setText(ui_styles.STATUS_MESSAGES['fullscreen'])
    
    def exit_fullscreen(self):
        """Exit fullscreen mode"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            if self.fullscreen_widget:
                self.fullscreen_widget.close()
                self.fullscreen_widget = None
            # Restore video to main window
            if sys.platform.startswith('win'):
                self.video_player.media_player.set_hwnd(self.video_frame.winId())
            self.status_label.setText(ui_styles.STATUS_MESSAGES['exit_fullscreen'])
            # Restore focus to main window
            self.setFocus()
    
    def video_frame_clicked(self, event):
        """Handle clicks on video frame to ensure focus"""
        self.setFocus()  # Set focus to main window for keyboard events
    
    def handle_escape(self):
        """Handle escape key press"""
        if self.is_fullscreen:
            self.exit_fullscreen()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    player = VLCPlayerGUI()
    player.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())