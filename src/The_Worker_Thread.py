import difflib
import re
from PyQt6.QtCore import QThread, pyqtSignal
from The_Audio_Engine import VoiceEngine

class VoiceWorker(QThread):
    command_found = pyqtSignal(object)  # Changed to object to support both str and dict
    finished_processing = pyqtSignal()
    transcription_done = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.engine = VoiceEngine()
        
        # Enhanced command dictionary with variations
        self.command_map = {
            "play": ["play", "start", "resume", "begin"],
            "pause": ["pause", "hold", "wait","boss"],
            "faster": ["faster", "speed up", "fast", "quick"],
            "slower": ["slower", "slow down", "slow"],
            "normal": ["normal speed", "normal", "regular speed", "default speed"],
            "volume up": ["volume up", "louder", "increase volume", "turn up"],
            "volume down": ["volume down", "quieter", "decrease volume", "turn down", "lower volume"],
            "mute": ["mute", "silence", "quiet", "no sound"]
        }
        
        # Flatten command variations for matching
        self.all_variations = []
        for cmd, variations in self.command_map.items():
            self.all_variations.extend(variations)

    def run(self):
        raw_text = self.engine.record_and_transcribe(duration=4)
        
        if raw_text:
            # Emit the raw transcription for debugging
            self.transcription_done.emit(raw_text)
            
            # Clean and normalize text
            clean_text = raw_text.replace(".", "").replace(",", "").replace("!", "").replace("?", "").strip()
            
            # First, check if it's a time jump command
            time_command = self._parse_time_jump(clean_text)
            if time_command:
                print(f"✅ Time jump: {time_command}")
                self.command_found.emit(time_command)
            # Second, check if it's a volume command with percentage
            elif volume_command := self._parse_volume_command(clean_text):
                print(f"✅ Volume command: {volume_command}")
                self.command_found.emit(volume_command)
            else:
                # Try to find regular command in the text
                command = self._match_command(clean_text)
                
                if command:
                    print(f"✅ Matched command: '{command}'")
                    self.command_found.emit(command)
                else:
                    print(f"❌ No command matched for: '{clean_text}'")
        
        self.finished_processing.emit()
    
    def _parse_time_jump(self, text):
        """Parse time jump commands like 'go to 1 hour 30 minutes' or 'jump to 2:30:15'"""
        text_lower = text.lower()
        
        # Check for time jump keywords
        time_keywords = ["go to", "jump to", "skip to", "seek to", "go", "jump"]
        has_time_keyword = any(keyword in text_lower for keyword in time_keywords)
        
        if not has_time_keyword:
            return None
        
        total_ms = 0
        
        # Pattern 1: "X hour(s) Y minute(s) Z second(s)"
        # Extract hours
        hour_match = re.search(r'(\d+)\s*(?:hour|hours|hr|hrs)', text_lower)
        if hour_match:
            total_ms += int(hour_match.group(1)) * 3600000
        
        # Extract minutes
        min_match = re.search(r'(\d+)\s*(?:minute|minutes|min|mins)', text_lower)
        if min_match:
            total_ms += int(min_match.group(1)) * 60000
        
        # Extract seconds
        sec_match = re.search(r'(\d+)\s*(?:second|seconds|sec|secs)', text_lower)
        if sec_match:
            total_ms += int(sec_match.group(1)) * 1000
        
        # Pattern 2: "HH:MM:SS" or "MM:SS" format
        if total_ms == 0:
            time_format = re.search(r'(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?', text_lower)
            if time_format:
                hours = 0
                minutes = 0
                seconds = 0
                
                if time_format.group(3):  # HH:MM:SS
                    hours = int(time_format.group(1))
                    minutes = int(time_format.group(2))
                    seconds = int(time_format.group(3))
                else:  # MM:SS
                    minutes = int(time_format.group(1))
                    seconds = int(time_format.group(2))
                
                total_ms = (hours * 3600000) + (minutes * 60000) + (seconds * 1000)
        
        # Pattern 3: Just numbers (assume minutes if single number)
        if total_ms == 0:
            number_match = re.search(r'\b(\d+)\b', text_lower)
            if number_match and ("minute" in text_lower or "min" in text_lower):
                total_ms = int(number_match.group(1)) * 60000
        
        if total_ms > 0:
            return {"time_ms": total_ms}
        
        return None
    
    def _parse_volume_command(self, text):
        """Parse volume commands like 'volume 50 percent' or 'set volume to 75'"""
        text_lower = text.lower()
        
        # Check for volume keywords
        volume_keywords = ["volume", "sound"]
        has_volume_keyword = any(keyword in text_lower for keyword in volume_keywords)
        
        if not has_volume_keyword:
            return None
        
        # Pattern 1: "volume X percent" or "volume X%"
        percent_match = re.search(r'(\d+)\s*(?:percent|%)', text_lower)
        if percent_match:
            volume = int(percent_match.group(1))
            volume = max(0, min(100, volume))  # Clamp between 0-100
            return {"volume_percent": volume}
        
        # Pattern 2: "volume X" or "set volume X" (assume it's percentage)
        volume_match = re.search(r'volume\s+(?:to\s+)?(\d+)', text_lower)
        if volume_match:
            volume = int(volume_match.group(1))
            volume = max(0, min(100, volume))  # Clamp between 0-100
            return {"volume_percent": volume}
        
        # Pattern 3: "set sound to X"
        sound_match = re.search(r'sound\s+(?:to\s+)?(\d+)', text_lower)
        if sound_match:
            volume = int(sound_match.group(1))
            volume = max(0, min(100, volume))  # Clamp between 0-100
            return {"volume_percent": volume}
        
        return None
    
    def _match_command(self, text):
        """Smart command matching with multiple strategies"""
        text_lower = text.lower()
        
        # Strategy 1: Exact phrase match
        for command, variations in self.command_map.items():
            for variation in variations:
                if variation in text_lower:
                    return command
        
        # Strategy 2: Check if command words appear in transcription
        for command, variations in self.command_map.items():
            for variation in variations:
                words = variation.split()
                if all(word in text_lower for word in words):
                    return command
        
        # Strategy 3: Fuzzy matching with lower threshold
        matches = difflib.get_close_matches(text_lower, self.all_variations, n=1, cutoff=0.5)
        if matches:
            # Find which command this variation belongs to
            for command, variations in self.command_map.items():
                if matches[0] in variations:
                    return command
        
        # Strategy 4: Word-by-word matching
        text_words = text_lower.split()
        for word in text_words:
            for command, variations in self.command_map.items():
                for variation in variations:
                    if word == variation or difflib.SequenceMatcher(None, word, variation).ratio() > 0.75:
                        return command
        
        return None