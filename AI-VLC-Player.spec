# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect transformers model files and tokenizers
datas = []
datas += collect_data_files('transformers')
datas += collect_data_files('tokenizers')
datas += collect_data_files('torch')

# Collect all torch and transformers submodules
hiddenimports = []
hiddenimports += collect_submodules('transformers')
hiddenimports += collect_submodules('torch')
hiddenimports += collect_submodules('tokenizers')
hiddenimports += collect_submodules('sounddevice')
hiddenimports += collect_submodules('numpy')

# Add specific imports that PyInstaller might miss
hiddenimports += [
    'transformers.models.whisper',
    'transformers.models.whisper.modeling_whisper',
    'transformers.models.whisper.tokenization_whisper',
    'transformers.models.whisper.tokenization_whisper_fast',
    'transformers.pipelines.audio_classification',
    'transformers.pipelines.automatic_speech_recognition',
    'torch.nn',
    'torch.nn.functional',
    'sounddevice',
    '_sounddevice',
    'queue',
    'scipy',
    'scipy.io',
    'scipy.io.wavfile',
    'The_Audio_Engine',
    'The_Worker_Thread',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AI-VLC-Player',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Changed to True to see voice control debug messages
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
