import sounddevice as sd
import numpy as np
import torch
from transformers import pipeline
import queue

# CONFIGURATION
SAMPLE_RATE = 16000
BLOCK_SIZE = 24000  # 1.5 seconds per chunk (Balance between latency and context)
SILENCE_THRESHOLD = 0.01 # Sensitivity (Adjust if mic is noisy)

# THE QUEUE (Thread-safe bridge)
audio_queue = queue.Queue()

class VoiceEngine:
    def __init__(self):
        print("Loading Whisper Model (tiny.en)...")
        # tiny.en is optimized for English commands (faster/better than base)
        self.asr = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-tiny.en",
            device="cpu" 
        )
        print("Whisper Loaded.")

    def audio_callback(self, indata, frames, time, status):
        """
        Runs in a background thread by sounddevice.
        Pushes audio to queue instantly.
        """
        if status:
            print(status)
        # Copy data to avoid buffer issues
        audio_queue.put(indata.copy())

    def start_listening(self):
        # Determine your input device index if needed, otherwise default
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            blocksize=BLOCK_SIZE,
            callback=self.audio_callback,
            dtype="float32"
        )
        self.stream.start()

    def stop_listening(self):
        self.stream.stop()
        self.stream.close()

    def process_queue(self):
        """
        Pulls audio, checks for silence, then transcribes.
        Returns: text or None
        """
        if audio_queue.empty():
            return None

        # Get audio block
        audio_data = audio_queue.get()
        
        # 1. Cheap VAD (Voice Activity Detection)
        # If audio is too quiet, discard it to save CPU
        volume = np.linalg.norm(audio_data) * 10
        if volume < SILENCE_THRESHOLD:
            return None

        # 2. Transcribe (Flatten array for Whisper)
        # Squeeze removes dimensions to make it a flat 1D array
        audio_flat = np.squeeze(audio_data)
        
        try:
            result = self.asr(audio_flat)
            text = result["text"].lower().strip()
            
            # 3. Hallucination Filter
            # Whisper sometimes outputs "you" or "." on silence. Filter short garbage.
            if len(text) < 2: 
                return None
                
            return text
        except Exception as e:
            print(f"Transcription error: {e}")
            return None