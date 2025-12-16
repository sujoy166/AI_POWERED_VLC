from PyQt6.QtWidgets import QMainWindow
from The_Worker_Thread import WhisperWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... setup UI ...
        
        # START THE EAR
        self.voice_thread = WhisperWorker()
        self.voice_thread.command_detected.connect(self.handle_voice)
        self.voice_thread.start()

    def handle_voice(self, text):
        """
        Logic Gate: Only allows specific commands through.
        """
        # 1. Sanitize
        # Remove punctuation that might mess up matching
        clean_text = text.replace(".", "").replace("!", "").replace("?", "")

        # 2. Wake Word Check (Optional but recommended)
        # If you want "Always on" mode, remove this block.
        # if "player" not in clean_text:
        #    return

        # 3. Command Mapping
        # We use 'in' to catch "pause video" or "pause now"
        if "play" in clean_text or "resume" in clean_text:
            self.do_play()
            
        elif "pause" in clean_text or "stop" in clean_text:
            self.do_pause()
            
        elif "fast" in clean_text or "speed up" in clean_text:
            self.player.set_rate(1.5)
            
        elif "slow" in clean_text:
            self.player.set_rate(0.7)
            
        elif "normal" in clean_text or "reset" in clean_text:
            self.player.set_rate(1.0)

        # 4. Volume logic (Handling numbers is hard, keep it simple)
        elif "louder" in clean_text or "volume up" in clean_text:
            self.change_volume(10)
            
        elif "quieter" in clean_text or "volume down" in clean_text:
            self.change_volume(-10)

    def do_play(self):
        # Your VLC logic
        pass

    def do_pause(self):
        # Your VLC logic
        pass
        
    def change_volume(self, amount):
        # Your VLC logic
        pass

    def closeEvent(self, event):
        # CRITICAL: Kill thread cleanly or app will hang in background
        self.voice_thread.stop()
        super().closeEvent(event)