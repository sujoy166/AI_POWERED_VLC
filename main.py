#!/usr/bin/env python3
"""
AI-VLC Player - A modern, feature-rich media player
Entry point for the application

Author: AI Assistant
Version: 2.0
Features: 
- Modern UI with dark theme
- Voice control with Whisper AI
- Fullscreen video-only mode
- Keyboard shortcuts (Space, F11, Escape)
- Multiple video format support
- Professional styling
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main_gui import VLCPlayerGUI
from PyQt6.QtWidgets import QApplication

def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    window = VLCPlayerGUI()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())