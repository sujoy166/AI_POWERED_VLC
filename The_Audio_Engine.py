import sounddevice as sd
import numpy as np
import torch
from transformers import pipeline
import queue

# CONFIGURATION
SAMPLE_RATE = 16000
BLOCK_SIZE = 24000  # 1.5 seconds per chunk (Balance between latency and context)
SILENCE_THRESHOLD = 0.001  # LOWERED for better sensitivity (was 0.01)

# THE QUEUE (Thread-safe bridge)
audio_queue = queue.Queue()

class VoiceEngine:
    def __init__(self):
        print("\n" + "="*50)
        print("🎤 VOICE ENGINE INITIALIZATION")
        print("="*50)
        
        # List available audio devices
        print("\n📋 Available Audio Devices:")
        print(sd.query_devices())
        
        # Get default input device
        default_device = sd.query_devices(kind='input')
        print(f"\n✓ Using Default Input Device:")
        print(f"  Name: {default_device['name']}")
        print(f"  Channels: {default_device['max_input_channels']}")
        print(f"  Sample Rate: {SAMPLE_RATE} Hz")
        
        print("\n🤖 Loading Whisper Model (tiny.en)...")
        print("   (This may take 30-60 seconds on first run)")
        # tiny.en is optimized for English commands (faster/better than base)
        self.asr = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-tiny.en",
            device="cpu",
            chunk_length_s=30,
            stride_length_s=5
        )
        print("✓ Whisper Model Loaded Successfully!")
        print("="*50 + "\n")

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
        
        # 1. Voice Activity Detection with DEBUG
        volume = np.linalg.norm(audio_data) * 10
        
        # Debug: Print volume level every time (helps diagnose mic issues)
        print(f"🔊 Audio Level: {volume:.4f} (Threshold: {SILENCE_THRESHOLD})")
        
        if volume < SILENCE_THRESHOLD:
            print("   ⚠️  Too quiet - ignored")
            return None
        
        print(f"   ✓ Voice detected! Processing...")

        # 2. Transcribe (Flatten array for Whisper)
        audio_flat = np.squeeze(audio_data)
        
        try:
            result = self.asr(audio_flat)
            text = result["text"].lower().strip()
            
            print(f"   🎤 Transcribed: '{text}'")
            
            # 3. Hallucination Filter
            if len(text) < 2: 
                print(f"   ⚠️  Too short - ignored")
                return None
                
            return text
        except Exception as e:
            print(f"   ❌ Transcription error: {e}")
            return None