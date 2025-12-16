# video_player.py - Core video playback functionality
import os
import sys
import vlc
from PyQt6.QtCore import QTimer, pyqtSignal, QObject

# Configure VLC path for Windows
if sys.platform.startswith('win'):
    # Common VLC installation paths
    vlc_paths = [
        r"C:\Program Files\VideoLAN\VLC",
        r"C:\Program Files (x86)\VideoLAN\VLC"
    ]
    
    vlc_path = None
    for path in vlc_paths:
        if os.path.exists(path):
            vlc_path = path
            break
    
    if vlc_path:
        os.environ['PATH'] = vlc_path + os.pathsep + os.environ.get('PATH', '')
        os.add_dll_directory(vlc_path)
    else:
        print("Warning: VLC installation not found in common locations")


class VideoPlayer(QObject):
    """Core video player functionality using VLC"""
    position_changed = pyqtSignal(int)
    duration_changed = pyqtSignal(int)
    state_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        
    def load_video(self, file_path):
        """Load and start playing a video file"""
        media = self.instance.media_new(file_path)
        self.media_player.set_media(media)
        self.media_player.play()
        self.timer.start(100)  # Update UI every 100ms
        
    def play(self):
        """Start or resume video playback"""
        self.media_player.play()
        
    def pause(self):
        """Pause video playback"""
        self.media_player.pause()
        
    def stop(self):
        """Stop video playback"""
        self.media_player.stop()
        
    def set_position(self, position):
        """Set playback position (0-1000)"""
        self.media_player.set_position(position / 1000.0)
        
    def set_volume(self, volume):
        """Set playback volume (0-100)"""
        self.media_player.audio_set_volume(volume)
    
    def set_rate(self, rate):
        """Set playback speed (0.5 = half speed, 2.0 = double speed)"""
        self.media_player.set_rate(rate)
    
    def get_rate(self):
        """Get current playback speed"""
        return self.media_player.get_rate()
        
    def update_ui(self):
        """Update UI with current playback position"""
        if self.media_player.is_playing():
            position = int(self.media_player.get_position() * 1000)
            self.position_changed.emit(position)