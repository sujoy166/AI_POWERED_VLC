"""
Microphone Test Utility
Run this to test if your microphone is working properly
"""

import sounddevice as sd
import numpy as np
import sys

print("\n" + "="*60)
print("🎤 MICROPHONE TEST UTILITY")
print("="*60)

print("\n1. Listing all audio devices...")
print("-" * 60)
devices = sd.query_devices()
print(devices)

print("\n2. Default input device:")
print("-" * 60)
try:
    default_input = sd.query_devices(kind='input')
    print(f"Name: {default_input['name']}")
    print(f"Max Input Channels: {default_input['max_input_channels']}")
    print(f"Default Sample Rate: {default_input['default_samplerate']}")
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("No input device found! Please check:")
    print("  - Is a microphone connected?")
    print("  - Is the microphone enabled in Windows Settings?")
    sys.exit(1)

print("\n3. Testing microphone input...")
print("-" * 60)
print("🎙️  Speak into your microphone for 3 seconds...")
print("   You should see volume levels appear below.\n")

SAMPLE_RATE = 16000
DURATION = 3  # seconds

try:
    # Record audio
    audio = sd.rec(int(DURATION * SAMPLE_RATE), 
                   samplerate=SAMPLE_RATE, 
                   channels=1, 
                   dtype='float32')
    
    # Show live volume meter
    for i in range(30):  # 30 updates in 3 seconds
        sd.sleep(100)  # 100ms
        
        # Calculate current volume
        current_chunk = audio[i*1600:(i+1)*1600]  # 100ms chunk
        if len(current_chunk) > 0:
            volume = np.linalg.norm(current_chunk) * 10
            
            # Create visual bar
            bar_length = int(volume * 100)
            bar = "█" * min(bar_length, 50)
            
            print(f"Volume: {volume:.4f} {bar}", end='\r')
    
    sd.wait()  # Wait for recording to finish
    
    # Calculate overall statistics
    volume_avg = np.linalg.norm(audio) * 10 / len(audio)
    volume_max = np.max(np.abs(audio)) * 10
    
    print("\n\n4. Test Results:")
    print("-" * 60)
    print(f"✓ Recording completed successfully!")
    print(f"  Average Volume: {volume_avg:.6f}")
    print(f"  Maximum Volume: {volume_max:.4f}")
    
    print("\n5. Diagnosis:")
    print("-" * 60)
    
    THRESHOLD = 0.001  # Current threshold in The_Audio_Engine.py
    
    if volume_max > THRESHOLD * 10:
        print(f"✅ EXCELLENT! Your microphone is working great!")
        print(f"   Voice commands should work perfectly.")
    elif volume_max > THRESHOLD:
        print(f"✓ GOOD! Your microphone is working.")
        print(f"   Speak clearly and closer to the mic for best results.")
    elif volume_max > THRESHOLD / 10:
        print(f"⚠️  WARNING! Microphone volume is very low.")
        print(f"   Current max: {volume_max:.6f}")
        print(f"   Threshold:   {THRESHOLD:.6f}")
        print(f"\n   Solutions:")
        print(f"   1. Increase microphone volume in Windows Settings")
        print(f"   2. Speak louder and closer to the microphone")
        print(f"   3. Check if microphone boost is enabled")
    else:
        print(f"❌ PROBLEM! Microphone is too quiet or not working.")
        print(f"   Current max: {volume_max:.6f}")
        print(f"   Threshold:   {THRESHOLD:.6f}")
        print(f"\n   Solutions:")
        print(f"   1. Check Windows microphone settings")
        print(f"   2. Ensure microphone is not muted")
        print(f"   3. Try a different microphone")
        print(f"   4. Enable microphone boost (100%)")
        print(f"   5. Grant microphone permissions to Python")

    print("\n6. Windows Settings Check:")
    print("-" * 60)
    print("   Go to: Settings > Privacy > Microphone")
    print("   Ensure: 'Allow apps to access your microphone' is ON")
    print("   Also check: Settings > System > Sound > Input")
    print("   Test your microphone and adjust volume there")
    
except Exception as e:
    print(f"\n❌ ERROR during recording: {e}")
    print("\nPossible issues:")
    print("  - Microphone not connected")
    print("  - Microphone permissions not granted")
    print("  - Microphone disabled in Windows")

print("\n" + "="*60)
print("Test completed!")
print("="*60 + "\n")

input("Press Enter to exit...")
