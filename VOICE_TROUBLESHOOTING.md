# 🎤 Voice Recognition Troubleshooting Guide

## Quick Fixes (Try These First!)

### 1. **Run Microphone Test**
```bash
python test_microphone.py
```
This will show you if your microphone is detected and working.

### 2. **Check Windows Microphone Settings**

#### Enable Microphone Access:
1. Open **Settings** → **Privacy & Security** → **Microphone**
2. Turn ON "Microphone access"
3. Turn ON "Let apps access your microphone"
4. Scroll down and ensure Python/Your app can access microphone

#### Increase Microphone Volume:
1. Right-click **Speaker icon** in taskbar
2. Click **Open Sound Settings**
3. Click **Input** → Select your microphone
4. Click **Device Properties**
5. Set **Volume to 100%**
6. Enable **Microphone Boost** if available

### 3. **Test Microphone in Windows**
1. Settings → System → Sound → Input
2. Click "Test your microphone"
3. Speak and watch the blue bar - it should move
4. If it doesn't move, your mic isn't working in Windows

## Common Issues & Solutions

### ❌ "No audio detected" / Volume always 0.0000

**Solution 1: Increase Sensitivity**
The audio threshold might be too high. Edit `The_Audio_Engine.py`:
```python
SILENCE_THRESHOLD = 0.0001  # Lower = more sensitive (was 0.001)
```

**Solution 2: Check Microphone Selection**
Windows might be using the wrong microphone:
1. Open Sound Settings
2. Under "Input", select the correct microphone from dropdown
3. Test it by speaking - the blue bar should move

**Solution 3: Grant Permissions**
```
Settings → Privacy → Microphone → Allow access
```

### ❌ "Microphone not detected"

**Check if microphone is connected:**
1. Physical connection (USB/Jack)
2. Bluetooth microphone paired
3. Headset microphone enabled

**Update audio drivers:**
1. Device Manager → Audio inputs and outputs
2. Right-click your microphone → Update driver

### ❌ Voice detected but not transcribed

**Solution: Speak louder and clearer**
- Speak at normal conversation volume
- Reduce background noise
- Position microphone closer (6-12 inches)

**Check language:**
- Whisper tiny.en only supports English
- Speak in English for best results

### ❌ Commands not recognized

**Make sure you're saying the right commands:**
- "Play" or "Resume" (not "start playing")
- "Pause" (not "hold" or "wait")
- "Louder" or "Volume up" (not "increase sound")

**Full command list in README.md**

## Advanced Troubleshooting

### Check Audio Device Selection

Add this to `The_Audio_Engine.py` to select specific device:

```python
def start_listening(self, device_index=None):
    # List devices first
    print(sd.query_devices())
    
    self.stream = sd.InputStream(
        device=device_index,  # Use specific device (e.g., 1, 2, 3)
        samplerate=SAMPLE_RATE,
        channels=1,
        blocksize=BLOCK_SIZE,
        callback=self.audio_callback,
        dtype="float32"
    )
    self.stream.start()
```

### Adjust Audio Settings

In `The_Audio_Engine.py`, try these adjustments:

```python
# For better sensitivity:
SILENCE_THRESHOLD = 0.0001  # Lower = more sensitive

# For longer recording (better accuracy):
BLOCK_SIZE = 32000  # 2 seconds (was 24000)

# For noisy environments:
SILENCE_THRESHOLD = 0.01  # Higher = less sensitive to noise
```

### Enable More Debug Info

The updated `The_Audio_Engine.py` now shows:
- Audio level for each chunk
- Whether voice was detected
- Transcription results
- Any errors

Watch the console for output like:
```
🔊 Audio Level: 0.0234 (Threshold: 0.001)
   ✓ Voice detected! Processing...
   🎤 Transcribed: 'play video'
```

### Use External Microphone

Built-in laptop mics are often poor quality:
1. Use USB microphone
2. Use headset with boom mic
3. Use Bluetooth headset
4. Position closer to mouth

## Testing Steps

### Step 1: System Level Test
1. Open Windows Sound Settings
2. Test microphone - blue bar should move when speaking
3. If no movement → Windows isn't detecting mic

### Step 2: Python Level Test
```bash
python test_microphone.py
```
Watch for:
- Device list (your mic should appear)
- Volume levels when speaking
- Diagnosis results

### Step 3: Application Test
1. Run `python main.py`
2. Watch for:
   - "✓ Whisper Model Loaded Successfully!"
   - "Microphone is LIVE."
   - Green "Voice Control: ACTIVE"
3. Speak clearly and watch console for "🔊 Audio Level" messages

## Still Not Working?

### Check These:

1. **Microphone Muted?**
   - Check physical mute button on headset
   - Check Windows mute button
   - Check app volume mixer

2. **Permissions?**
   - Windows Privacy Settings
   - Antivirus blocking microphone access
   - Administrator rights needed?

3. **Driver Issues?**
   - Update audio drivers
   - Reinstall audio drivers
   - Restart computer

4. **Wrong Device?**
   - Multiple microphones connected
   - System using wrong one
   - Disable unused microphones

### Get Device List

Run this in Python to see all devices:
```python
import sounddevice as sd
print(sd.query_devices())
```

Find your microphone's index number and use it in the code.

## Contact & Support

If nothing works:
1. Run `test_microphone.py` and save the output
2. Check console output when running the app
3. Report issue with:
   - Device list from test
   - Volume levels detected
   - Error messages (if any)

---

**Most Common Fix:** Increase Windows microphone volume to 100% and enable microphone boost! 🎤
