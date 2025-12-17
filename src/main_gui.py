import os
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QSlider, QLabel, 
                            QFileDialog, QMessageBox, QFrame, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut

# Import our custom modules
from video_player import VideoPlayer
from fullscreen_widget import FullscreenVideoWidget
from The_Worker_Thread import VoiceWorker
import ui_styles


class VLCPlayerGUI(QMainWindow):
    """Main GUI window for the AI-VLC Player"""
    
    def __init__(self):
        super().__init__()
        self.video_player = VideoPlayer()
        self.current_file = None
        self.is_fullscreen = False
        self.fullscreen_widget = None
        
        # Voice control setup
        self.voice_thread = VoiceWorker() # Initialize the worker
        self.is_recording = False
        self.slider_being_dragged = False
        
        self.init_ui()
        self.connect_signals()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("AI-VLC Player")
        self.setGeometry(100, 100, 900, 650)
        self.setStyleSheet(ui_styles.MAIN_WINDOW_STYLE)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Video display area
        self.video_frame = QWidget()
        self.video_frame.setStyleSheet(ui_styles.VIDEO_FRAME_STYLE)
        self.video_frame.setMinimumHeight(420)
        self.video_frame.mouseDoubleClickEvent = self.toggle_fullscreen
        main_layout.addWidget(self.video_frame)
        
        # Controls area
        controls_layout = QVBoxLayout()
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setRange(0, 1000)
        self.progress_slider.setStyleSheet(ui_styles.PROGRESS_SLIDER_STYLE)
        controls_layout.addWidget(self.progress_slider)
        
        buttons_layout = QHBoxLayout()
        self.open_btn = QPushButton(ui_styles.BUTTON_TEXTS['open'])
        self.play_btn = QPushButton(ui_styles.BUTTON_TEXTS['play'])
        self.pause_btn = QPushButton(ui_styles.BUTTON_TEXTS['pause'])
        self.settings_btn = QPushButton("⚙ Settings")
        
        for btn in [self.open_btn, self.play_btn, self.pause_btn, self.settings_btn]:
            btn.setStyleSheet(ui_styles.BUTTON_STYLE)
        
        buttons_layout.addWidget(self.open_btn)
        buttons_layout.addWidget(self.play_btn)
        buttons_layout.addWidget(self.pause_btn)
        buttons_layout.addWidget(self.settings_btn)
        buttons_layout.addStretch()
        
        # Timestamp display
        self.timestamp_label = QLabel("00:00:00 / 00:00:00")
        self.timestamp_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; padding: 5px;")
        buttons_layout.addWidget(self.timestamp_label)
        
        # Volume control (vertical)
        volume_container = QVBoxLayout()
        volume_label = QLabel("🔊")
        volume_label.setStyleSheet("color: white; font-size: 18px;")
        volume_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        volume_container.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Orientation.Vertical)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setMaximumHeight(100)
        self.volume_slider.setMinimumHeight(80)
        self.volume_slider.setStyleSheet(ui_styles.VOLUME_SLIDER_STYLE)
        volume_container.addWidget(self.volume_slider)
        
        # Volume percentage display
        self.volume_percent_label = QLabel("50%")
        self.volume_percent_label.setStyleSheet("color: white; font-weight: bold; font-size: 11px;")
        self.volume_percent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        volume_container.addWidget(self.volume_percent_label)
        
        buttons_layout.addLayout(volume_container)
        
        controls_layout.addLayout(buttons_layout)
        
        # Status
        self.status_label = QLabel(ui_styles.STATUS_MESSAGES['ready'])
        self.status_label.setStyleSheet(ui_styles.STATUS_LABEL_STYLE)
        controls_layout.addWidget(self.status_label)
        
        # UPDATED: Voice control UI
        voice_indicator_layout = QHBoxLayout()
        self.voice_status_label = QLabel("🎤 Whisper Engine: Standby")
        self.voice_status_label.setStyleSheet("color: #888888; font-weight: bold;")
        voice_indicator_layout.addWidget(self.voice_status_label)
        voice_indicator_layout.addStretch()
        
        # The Push-to-Talk Button
        self.voice_cmd_btn = QPushButton("🎤 Hold to Speak")
        self.voice_cmd_btn.setStyleSheet(ui_styles.BUTTON_STYLE)
        self.voice_cmd_btn.setMinimumWidth(150)
        # Connect to the recording trigger
        self.voice_cmd_btn.clicked.connect(self.start_voice_recording)
        
        voice_indicator_layout.addWidget(self.voice_cmd_btn)
        controls_layout.addLayout(voice_indicator_layout)
        
        main_layout.addLayout(controls_layout)
        
        if sys.platform.startswith('win'):
            self.video_player.media_player.set_hwnd(self.video_frame.winId())
        
        # Initialize volume
        initial_volume = self.volume_slider.value()
        self.video_player.set_volume(initial_volume)
        
        # Setup keyboard shortcuts
        self.space_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        self.space_shortcut.activated.connect(self.toggle_play_pause)
        
        self.f11_shortcut = QShortcut(QKeySequence(Qt.Key.Key_F11), self)
        self.f11_shortcut.activated.connect(self.toggle_fullscreen)
        
        # Enable key event handling
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def keyPressEvent(self, event):
        """Handle keyboard events in main window"""
        if event.key() == Qt.Key.Key_Space:
            self.toggle_play_pause()
            event.accept()
        elif event.key() == Qt.Key.Key_F11:
            self.toggle_fullscreen()
            event.accept()
        else:
            super().keyPressEvent(event)

    def connect_signals(self):
        """Connect buttons and voice worker signals"""
        self.open_btn.clicked.connect(self.open_file)
        self.play_btn.clicked.connect(self.play_video)
        self.pause_btn.clicked.connect(self.pause_video)
        self.settings_btn.clicked.connect(self.show_settings)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.progress_slider.sliderMoved.connect(self.set_position)
        self.progress_slider.sliderPressed.connect(self.on_slider_pressed)
        self.progress_slider.sliderReleased.connect(self.on_slider_released)
        self.video_player.position_changed.connect(self.update_progress)
        self.video_player.duration_changed.connect(self.update_duration)

        # Voice Thread Signals
        self.voice_thread.command_found.connect(self.handle_voice_command)
        self.voice_thread.finished_processing.connect(self.reset_voice_ui)
        self.voice_thread.transcription_done.connect(self.show_transcription)

    def start_voice_recording(self):
        """Triggered by the button to start the 4-second window"""
        if not self.is_recording:
            self.is_recording = True
            self.voice_cmd_btn.setText("🔴 Listening... (4s)")
            self.voice_cmd_btn.setEnabled(False)
            self.voice_cmd_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
            self.voice_status_label.setText("🎤 Listening: Speak clearly now!")
            self.voice_status_label.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 13px;")
            
            # Update fullscreen voice status if in fullscreen
            if self.fullscreen_widget and hasattr(self.fullscreen_widget, 'voice_status'):
                self.fullscreen_widget.voice_status.setText("Listening...")
            
            self.voice_thread.start() # Runs the 4s recording logic in background
    
    def show_transcription(self, text):
        """Display what was heard"""
        self.voice_status_label.setText(f"🎤 Heard: '{text}'")
        self.voice_status_label.setStyleSheet("color: #3498db; font-weight: bold;")

    def reset_voice_ui(self):
        """Resets the button after recording/transcribing is done"""
        self.is_recording = False
        self.voice_cmd_btn.setText("🎤 Hold to Speak")
        self.voice_cmd_btn.setEnabled(True)
        self.voice_cmd_btn.setStyleSheet(ui_styles.BUTTON_STYLE)
        self.voice_status_label.setText("🎤 Whisper Engine: Standby")
        
        # Update fullscreen voice status if in fullscreen
        if self.fullscreen_widget and hasattr(self.fullscreen_widget, 'voice_status'):
            self.fullscreen_widget.voice_status.setText("Standby")

    def handle_voice_command(self, command):
        """Execute logic based on the fuzzy-matched command"""
        if not command:
            self.status_label.setText("❌ No command recognized")
            self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            return

        # Check if it's a time jump command (contains timestamp data)
        if isinstance(command, dict) and "time_ms" in command:
            self.jump_to_time(command["time_ms"])
            hours = command["time_ms"] // 3600000
            minutes = (command["time_ms"] % 3600000) // 60000
            seconds = (command["time_ms"] % 60000) // 1000
            self.status_label.setText(f"✅ Jumped to {hours:02d}:{minutes:02d}:{seconds:02d}")
            self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold; font-size: 14px;")
            return
        
        # Check if it's a volume percentage command
        if isinstance(command, dict) and "volume_percent" in command:
            volume = command["volume_percent"]
            self.volume_slider.setValue(volume)
            self.status_label.setText(f"✅ Volume set to {volume}%")
            self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold; font-size: 14px;")
            return

        self.status_label.setText(f"✅ Executing: {command.upper()}")
        self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold; font-size: 14px;")
        
        if command == "play":
            self.play_video()
        elif command == "pause":
            self.pause_video()
        elif command == "faster":
            self.set_speed(1.5)
        elif command == "normal":
            self.set_speed(1.0)
        elif command == "slower":
            self.set_speed(0.5)
        elif command == "volume up":
            val = min(100, self.volume_slider.value() + 10)
            self.volume_slider.setValue(val)
            self.status_label.setText(f"✅ Volume: {val}%")
        elif command == "volume down":
            val = max(0, self.volume_slider.value() - 10)
            self.volume_slider.setValue(val)
            self.status_label.setText(f"✅ Volume: {val}%")
        elif command == "mute":
            self.volume_slider.setValue(0)
            self.status_label.setText("✅ Muted")

    # ... (Keep existing open_file, play_video, pause_video, etc. methods) ...

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Videos (*.mp4 *.mkv *.avi)")
        if file_path:
            self.current_file = file_path
            self.status_label.setText(f"Loaded: {os.path.basename(file_path)}")

    def play_video(self):
        if self.current_file:
            self.video_player.load_video(self.current_file)
            self.status_label.setText("Playing...")
        else:
            QMessageBox.warning(self, "Warning", "Select a file first")

    def pause_video(self):
        self.video_player.pause()
        self.status_label.setText("Paused")

    def set_volume(self, volume):
        """Set volume and update display"""
        self.video_player.set_volume(volume)
        self.volume_percent_label.setText(f"{volume}%")
    
    def show_settings(self):
        """Show settings dialog with speed controls"""
        dialog = QDialog(self)
        dialog.setWindowTitle("⚙ Settings")
        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #E45A92, stop: 1 #D1477F);
            }
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        dialog.setMinimumWidth(350)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Playback Speed")
        title.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Speed buttons
        speed_slower_btn = QPushButton("🐢 Slower (0.5x)")
        speed_normal_btn = QPushButton("▶ Normal (1.0x)")
        speed_faster_btn = QPushButton("🐰 Faster (1.5x)")
        
        for btn in [speed_slower_btn, speed_normal_btn, speed_faster_btn]:
            btn.setStyleSheet(ui_styles.BUTTON_STYLE + "min-height: 40px; font-size: 14px;")
            layout.addWidget(btn)
        
        # Connect speed buttons
        speed_slower_btn.clicked.connect(lambda: self.set_speed(0.5))
        speed_normal_btn.clicked.connect(lambda: self.set_speed(1.0))
        speed_faster_btn.clicked.connect(lambda: self.set_speed(1.5))
        
        # Close button
        close_btn = QPushButton("✓ Close")
        close_btn.setStyleSheet(ui_styles.BUTTON_STYLE + "min-height: 35px; background-color: #2ecc71;")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec()

    def set_position(self, position):
        """Set video position from slider (0-1000)"""
        self.video_player.set_position(position)
        # Update timestamp immediately for smooth feedback
        duration = self.video_player.media_player.get_length()
        if duration > 0:
            new_time = int((position / 1000.0) * duration)
            self.timestamp_label.setText(f"{self.format_time(new_time)} / {self.format_time(duration)}")
    
    def on_slider_pressed(self):
        """Called when user starts dragging the slider"""
        self.slider_being_dragged = True
    
    def on_slider_released(self):
        """Called when user releases the slider"""
        self.slider_being_dragged = False
        # Set the final position when released
        position = self.progress_slider.value()
        self.set_position(position)
    
    def set_speed(self, rate):
        """Set playback speed"""
        self.video_player.media_player.set_rate(rate)
        self.status_label.setText(f"✅ Speed: {rate}x")
    
    def jump_to_time(self, time_ms):
        """Jump to specific time in milliseconds"""
        self.video_player.media_player.set_time(time_ms)
    
    def format_time(self, milliseconds):
        """Convert milliseconds to HH:MM:SS format"""
        if milliseconds < 0:
            return "00:00:00"
        seconds = milliseconds // 1000
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def update_progress(self, position):
        # Only update slider if user is not dragging it
        if not self.progress_slider.isSliderDown() and not self.slider_being_dragged:
            self.progress_slider.setValue(position)
        
        # Always update timestamp (unless user is actively dragging)
        if not self.slider_being_dragged:
            current_time = self.video_player.media_player.get_time()
            duration = self.video_player.media_player.get_length()
            self.timestamp_label.setText(f"{self.format_time(current_time)} / {self.format_time(duration)}")
    
    def update_duration(self, duration):
        """Update total duration display"""
        pass  # Duration is now shown in update_progress
    
    def toggle_play_pause(self):
        """Toggle between play and pause"""
        if self.video_player.media_player.is_playing():
            self.pause_video()
        else:
            # Resume playback from current position, don't reload
            if self.current_file:
                self.video_player.play()
                self.status_label.setText("Playing...")
            else:
                self.play_video()

    def toggle_fullscreen(self, event=None):
        if not self.current_file: return
        if self.is_fullscreen:
            self.exit_fullscreen()
        else:
            self.is_fullscreen = True
            self.fullscreen_widget = FullscreenVideoWidget(self.video_player.media_player, self)
    
    def exit_fullscreen(self):
        """Exit fullscreen mode and restore video to main window"""
        self.is_fullscreen = False
        if self.fullscreen_widget:
            self.fullscreen_widget.close()
            self.fullscreen_widget = None
        if sys.platform.startswith('win'):
            self.video_player.media_player.set_hwnd(self.video_frame.winId())
        self.show()
        self.activateWindow()

    def closeEvent(self, event):
        """Clean up resources when closing the application"""
        if self.voice_thread and self.voice_thread.isRunning():
            self.voice_thread.terminate()
            self.voice_thread.wait()
        if self.fullscreen_widget:
            self.fullscreen_widget.close()
        self.video_player.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VLCPlayerGUI()
    window.show()
    sys.exit(app.exec())