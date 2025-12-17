import sounddevice as sd
import numpy as np
from transformers import pipeline

class VoiceEngine:
    def __init__(self):
        # Using tiny.en for the fastest possible local execution
        self.asr = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-tiny.en",
            device="cpu",
            chunk_length_s=30
        )
        self.sample_rate = 16000

    def record_and_transcribe(self, duration=4):
        """Captures audio and converts to text with improved preprocessing."""
        try:
            # Record raw audio (increased to 4 seconds for better capture)
            recording = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32"
            )
            sd.wait()  # Block until hardware is done recording
            
            # Preprocess audio: Normalize and remove silence
            audio_flat = np.squeeze(recording)
            
            # Normalize audio to prevent clipping
            max_val = np.abs(audio_flat).max()
            if max_val > 0:
                audio_flat = audio_flat / max_val * 0.95
            
            # Apply basic noise gate - remove very quiet parts at start/end
            threshold = 0.01
            mask = np.abs(audio_flat) > threshold
            if mask.any():
                indices = np.where(mask)[0]
                start_idx = max(0, indices[0] - int(0.1 * self.sample_rate))
                end_idx = min(len(audio_flat), indices[-1] + int(0.1 * self.sample_rate))
                audio_flat = audio_flat[start_idx:end_idx]
            
            # Process with Whisper
            result = self.asr(audio_flat, return_timestamps=False)
            transcribed_text = result["text"].lower().strip()
            
            print(f"🎤 Transcribed: '{transcribed_text}'")  # Debug output
            return transcribed_text
            
        except Exception as e:
            print(f"Engine Error: {e}")
            return ""