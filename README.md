# 🎬 AI-VLC Player with Voice Control

A modern, feature-rich media player built with Python, PyQt6, and VLC, featuring **AI-powered voice control** using OpenAI's Whisper model.

## ✨ Features

### 🎥 Core Video Player
- **Modern Dark UI** - Beautiful, professional interface
- **Multiple Format Support** - MP4, AVI, MKV, MOV, WMV, FLV, WebM
- **Fullscreen Mode** - Immersive video-only viewing (F11)
- **Progress Control** - Visual timeline slider
- **Volume Control** - Easy volume adjustment
- **Playback Speed** - Control video speed (0.5x - 2.0x)

### 🎤 Voice Control (AI-Powered)
Control your media player using natural voice commands powered by OpenAI Whisper!

#### Playback Commands
- **"Play"** / **"Resume"** / **"Start"** - Start video playback
- **"Pause"** - Pause the video
- **"Stop"** - Stop playback

#### Navigation Commands
- **"Forward"** / **"Skip"** / **"Ahead"** - Skip forward 10 seconds
- **"Back"** / **"Backward"** / **"Rewind"** - Go back 10 seconds

#### Speed Control
- **"Fast"** / **"Faster"** / **"Speed up"** - Increase speed to 1.5x
- **"Slow"** / **"Slower"** / **"Slow down"** - Decrease speed to 0.7x
- **"Normal speed"** / **"Reset speed"** - Return to normal speed (1.0x)

#### Volume Control
- **"Louder"** / **"Volume up"** / **"Increase volume"** - Increase volume by 10%
- **"Quieter"** / **"Volume down"** / **"Lower"** - Decrease volume by 10%
- **"Mute"** - Set volume to 0%
- **"Unmute"** / **"Full volume"** - Set volume to 100%

#### Display Commands
- **"Fullscreen"** / **"Full screen"** - Enter fullscreen mode
- **"Exit fullscreen"** / **"Window mode"** - Exit fullscreen
- **"Open"** / **"Load"** / **"File"** - Open file dialog

### ⌨️ Keyboard Shortcuts
- **Space** - Toggle play/pause
- **Left Arrow** - Seek backward 10 seconds
- **Right Arrow** - Seek forward 10 seconds
- **F11** - Toggle fullscreen
- **Escape** - Exit fullscreen

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- VLC Media Player installed on your system

### Required Dependencies

```bash
pip install PyQt6 python-vlc sounddevice numpy torch transformers
```

### Dependency Breakdown
- **PyQt6** - Modern GUI framework
- **python-vlc** - VLC media player Python bindings
- **sounddevice** - Audio input capture
- **numpy** - Numerical operations for audio processing
- **torch** - PyTorch for deep learning
- **transformers** - Hugging Face Transformers (Whisper model)

## 🚀 Quick Start

1. **Clone or download** this repository

2. **Install dependencies:**
   ```bash
   pip install PyQt6 python-vlc sounddevice numpy torch transformers
   ```

3. **Ensure VLC is installed:**
   - Windows: Install from https://www.videolan.org/vlc/
   - The player will automatically detect VLC installation

4. **Run the application:**
   ```bash
   python main.py
   ```

5. **Start using voice commands!**
   - The microphone will activate automatically
   - Watch for the green "Voice Control: ACTIVE" indicator
   - Speak naturally - no wake word required!

## 📁 Project Structure

```
AI-VLC-Player/
├── main.py                    # Application entry point
├── main_gui.py               # Main GUI with voice integration
├── video_player.py           # VLC player core functionality
├── The_Audio_Engine.py       # Whisper voice recognition engine
├── The_Worker_Thread.py      # Background thread for voice processing
├── fullscreen_widget.py      # Fullscreen display handler
├── ui_styles.py             # UI styling and themes
├── Integration_with_audio.py # Voice integration example
└── README.md                # This file
```

## 🎯 How Voice Control Works

### Architecture
1. **Audio Capture** - Continuously captures microphone input (1.5 second chunks)
2. **Voice Activity Detection** - Filters out silence to save CPU
3. **Transcription** - Uses Whisper tiny.en model for English speech recognition
4. **Command Parsing** - Matches transcribed text to predefined commands
5. **Action Execution** - Executes corresponding player controls

### Whisper Model
- **Model**: OpenAI Whisper `tiny.en`
- **Optimized for**: English voice commands
- **Processing**: Real-time on CPU
- **Latency**: ~1.5 seconds per command

### Performance Tips
- Speak clearly and naturally
- Allow brief pauses between commands
- Check the status label for command feedback
- If commands aren't recognized, try rephrasing

## 🎛️ Voice Control Toggle

You can enable/disable voice control anytime:
- Click the **"🎤 Disable/Enable Voice"** button
- Voice status indicator shows current state:
  - 🟢 **Green** - Voice control active
  - ⚪ **Gray** - Voice control disabled
  - 🔴 **Red** - Error in voice control

## 🐛 Troubleshooting

### Voice Control Not Working
1. Check microphone permissions
2. Ensure microphone is not muted
3. Verify `sounddevice` installation
4. Check the voice status indicator for errors

### VLC Not Found
- Ensure VLC is installed in default locations:
  - `C:\Program Files\VideoLAN\VLC`
  - `C:\Program Files (x86)\VideoLAN\VLC`

### High CPU Usage
- Voice processing runs in background thread
- Normal usage: 5-15% CPU
- If higher: Try disabling voice control when not needed

### Model Download
- First run downloads Whisper model (~40MB)
- This happens automatically
- Requires internet connection

## 🔧 Configuration

### Audio Settings (in The_Audio_Engine.py)
```python
SAMPLE_RATE = 16000      # Audio sample rate (Hz)
BLOCK_SIZE = 24000       # Audio chunk size (1.5 seconds)
SILENCE_THRESHOLD = 0.01 # Voice detection sensitivity
```

### Adjust sensitivity if:
- **Too sensitive**: Increase `SILENCE_THRESHOLD` to 0.02
- **Not sensitive enough**: Decrease to 0.005

## 🌟 Advanced Usage

### Custom Voice Commands
Edit `handle_voice_command()` in `main_gui.py` to add custom commands:

```python
elif "your custom command" in clean_text:
    # Your custom action here
    self.status_label.setText("🎤 Voice: Custom action")
```

### Wake Word (Optional)
Uncomment in `handle_voice_command()` to require a wake word:

```python
if "player" not in clean_text:
    return  # Only process commands containing "player"
```

## 📝 System Requirements

### Minimum
- **CPU**: Dual-core 2.0 GHz
- **RAM**: 4 GB
- **OS**: Windows 10/11, Linux, macOS
- **Python**: 3.8+

### Recommended
- **CPU**: Quad-core 2.5 GHz+
- **RAM**: 8 GB+
- **GPU**: Optional (CPU works fine for tiny.en model)

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest new voice commands
- Improve UI/UX
- Optimize performance

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **VLC Media Player** - Powerful multimedia framework
- **OpenAI Whisper** - State-of-the-art speech recognition
- **PyQt6** - Excellent Python GUI framework
- **Hugging Face** - Transformers library and model hosting

## 📧 Support

For issues, questions, or feature requests, please create an issue in the repository.

---

**Enjoy your AI-powered media player! 🎬🎤**
