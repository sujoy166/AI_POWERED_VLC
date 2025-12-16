from PyQt6.QtCore import QThread, pyqtSignal
import time
from The_Audio_Engine import VoiceEngine
class WhisperWorker(QThread):
    command_detected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.engine = VoiceEngine()
        self.is_running = True

    def run(self):
        self.engine.start_listening()
        print("Microphone is LIVE.")
        
        while self.is_running:
            # Check the queue for new audio
            text = self.engine.process_queue()
            
            if text:
                print(f"Whisper heard: {text}") # Debugging
                self.command_detected.emit(text)
            
            # Tiny sleep prevents CPU spiking while waiting for Queue
            # We process faster than real-time, so this is safe.
            time.sleep(0.1)

    def stop(self):
        self.is_running = False
        self.engine.stop_listening()
        self.wait()