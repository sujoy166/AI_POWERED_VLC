# ui_styles.py - UI styling constants and themes
"""
UI styling constants for the AI-VLC Player
Contains all CSS styles, colors, and theming information
"""

# Main window styling - Korean soothing theme
MAIN_WINDOW_STYLE = """
QMainWindow {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                              stop: 0 #E45A92, stop: 1 #D1477F);
    color: #ffffff;
}
QWidget {
    background-color: transparent;
    color: #ffffff;
}
"""

# Video frame styling
VIDEO_FRAME_STYLE = """
QWidget {
    background-color: #000000;
    border: 2px solid #E45A92;
    border-radius: 8px;
}
"""

# Button styling - Korean soothing theme
BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                              stop: 0 #647FBC, stop: 1 #546BA8);
    border: none;
    border-radius: 6px;
    color: white;
    font-size: 12px;
    font-weight: bold;
    padding: 8px 16px;
    margin: 2px;
    min-width: 80px;
}
QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                              stop: 0 #7B93CC, stop: 1 #6A85BE);
}
QPushButton:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                              stop: 0 #546BA8, stop: 1 #485D95);
}
"""

# Progress slider styling - Korean soothing theme
PROGRESS_SLIDER_STYLE = """
QSlider::groove:horizontal {
    border: 1px solid #E45A92;
    height: 8px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #F0C1DA, stop:1 #E8ADD1);
    margin: 2px 0;
    border-radius: 4px;
}
QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #647FBC, stop:1 #546BA8);
    border: 1px solid #546BA8;
    width: 18px;
    margin: -5px 0;
    border-radius: 9px;
}
QSlider::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #7B93CC, stop:1 #6A85BE);
}
QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #647FBC, stop:1 #546BA8);
    border: 1px solid #546BA8;
    height: 8px;
    border-radius: 4px;
}
"""

# Volume slider styling - Korean soothing theme
VOLUME_SLIDER_STYLE = """
QSlider::groove:horizontal {
    border: 1px solid #E45A92;
    height: 6px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #F0C1DA, stop:1 #E8ADD1);
    margin: 2px 0;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #647FBC, stop:1 #546BA8);
    border: 1px solid #546BA8;
    width: 14px;
    margin: -4px 0;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #7B93CC, stop:1 #6A85BE);
}
QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #647FBC, stop:1 #546BA8);
    border: 1px solid #546BA8;
    height: 6px;
    border-radius: 3px;
}
"""

# Volume label styling
VOLUME_LABEL_STYLE = """
QLabel {
    color: #ffffff;
    font-size: 11px;
    font-weight: bold;
}
"""

# Status label styling - Korean soothing theme
STATUS_LABEL_STYLE = """
QLabel {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                              stop: 0 #F7D7E8, stop: 1 #F0C1DA);
    border: 1px solid #E45A92;
    border-radius: 5px;
    padding: 8px;
    color: #333333;
    font-size: 11px;
    font-weight: bold;
}
"""

# Button text with icons
BUTTON_TEXTS = {
    'open': '📁 Open File',
    'play': '▶️ Play',
    'pause': '⏸️ Pause',
    'stop': '⏹️ Stop'
}

# Status messages with icons
STATUS_MESSAGES = {
    'ready': '🎬 Ready to play video',
    'loaded': '📁 Loaded: {}',
    'playing': '▶️ Playing...',
    'paused': '⏸️ Paused',
    'stopped': '⏹️ Stopped',
    'fullscreen': 'Fullscreen mode - Press ESC or F11 to exit',
    'exit_fullscreen': 'Exited fullscreen mode',
    'load_first': 'Please load a video first'
}

# Tooltips
TOOLTIPS = {
    'open_btn': 'Browse and select a video file to play',
    'play_btn': 'Start playing the loaded video',
    'pause_btn': 'Pause the current video',
    'stop_btn': 'Stop playback and reset position',
    'progress_slider': 'Drag to seek through the video',
    'volume_slider': 'Adjust playback volume'
}