# Building the Executable

## Prerequisites

1. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify VLC is installed** on your system

## Build Methods

### Method 1: Using Build Script (Recommended)

Simply double-click `build_exe.bat` or run:
```bash
build_exe.bat
```

### Method 2: Manual Build

```bash
# Clean previous builds
pyinstaller AI-VLC-Player.spec --clean
```

## Build Time

- Expected build time: 5-10 minutes
- The process will collect all dependencies including:
  - PyQt6 GUI framework
  - VLC bindings
  - Whisper AI model
  - Torch deep learning framework
  - Audio processing libraries

## Output

After successful build:
- **Executable location:** `dist/AI-VLC-Player.exe`
- **Size:** Approximately 500MB-1GB (includes all dependencies)

## First Run

When you run the executable for the first time:

1. **Model Download** - Whisper tiny.en model (~40MB) will be downloaded automatically
2. **Internet Required** - First run requires internet connection
3. **Microphone Access** - Windows will ask for microphone permissions
4. **VLC Required** - Ensure VLC Media Player is installed

## Troubleshooting

### Build Errors

**Error: "Module not found"**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Error: "PyInstaller not found"**
```bash
pip install pyinstaller
```

### Runtime Errors

**Voice Control Not Working**
- Check microphone permissions in Windows Settings
- Ensure sounddevice is included in build
- Console window will show debug messages

**VLC Not Found**
- Install VLC Media Player from https://www.videolan.org/vlc/
- Default installation paths:
  - `C:\Program Files\VideoLAN\VLC`
  - `C:\Program Files (x86)\VideoLAN\VLC`

**Model Download Fails**
- Check internet connection
- Download may take 2-5 minutes
- Model is cached after first download

## Spec File Details

The `AI-VLC-Player.spec` file includes:

1. **Hidden Imports:**
   - All Whisper/Transformers modules
   - Torch neural network modules
   - Audio processing libraries
   - Custom modules (The_Audio_Engine, The_Worker_Thread)

2. **Data Files:**
   - Transformers model configurations
   - Tokenizer files
   - Torch library data

3. **Console Mode:**
   - Set to `True` for debugging
   - Shows voice command recognition in real-time
   - Change to `False` for production (no console window)

## Distribution

To distribute your executable:

1. **Include with EXE:**
   - The single `AI-VLC-Player.exe` file is self-contained
   - No additional files needed from `dist` folder

2. **User Requirements:**
   - Windows 10/11
   - VLC Media Player installed
   - Working microphone
   - Internet connection (first run only)

3. **File Size:**
   - Executable: ~500MB-1GB
   - This is normal for AI-powered applications
   - Size includes entire Python runtime + AI models

## Advanced Options

### Reduce Executable Size

Edit `AI-VLC-Player.spec` and add to `excludes`:
```python
excludes=['matplotlib', 'pandas', 'IPython'],
```

### Production Build (No Console)

Change in `AI-VLC-Player.spec`:
```python
console=False,  # No console window
```

### One-File vs One-Folder

Current configuration: **One-file** (everything in single .exe)

To create one-folder distribution (faster startup):
```bash
pyinstaller main.py --name "AI-VLC-Player" --onedir
```

## Performance Notes

- **Startup Time:** 5-15 seconds (includes AI model loading)
- **Memory Usage:** 500MB-1GB (AI models in memory)
- **Voice Recognition:** Real-time (~1.5s latency)
- **CPU Usage:** 5-20% during voice processing

## Build Script Contents

The `build_exe.bat` script:
1. Cleans previous builds
2. Runs PyInstaller with spec file
3. Verifies successful build
4. Shows output location and notes

## Questions?

For issues or questions about building, check:
1. PyInstaller logs in console output
2. `build/AI-VLC-Player/warn-AI-VLC-Player.txt` - Lists missing modules
3. GitHub issues page

---

**Ready to build?** Run `build_exe.bat` and wait for completion! 🚀
