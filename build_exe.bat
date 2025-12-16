@echo off
echo ========================================
echo Building AI-VLC Player Executable
echo ========================================
echo.
echo This will create an executable with voice control support.
echo Please wait, this may take 5-10 minutes...
echo.

REM Clean previous builds
echo [1/3] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the executable
echo [2/3] Building executable with PyInstaller...
pyinstaller AI-VLC-Player.spec --clean

REM Check if build was successful
if exist "dist\AI-VLC-Player.exe" (
    echo.
    echo ========================================
    echo Build completed successfully!
    echo ========================================
    echo.
    echo Executable location: dist\AI-VLC-Player.exe
    echo.
    echo IMPORTANT NOTES:
    echo - First run will download Whisper model (~40MB)
    echo - Requires internet connection for first run
    echo - Ensure VLC Media Player is installed
    echo - Microphone access required for voice control
    echo.
    pause
) else (
    echo.
    echo ========================================
    echo Build FAILED!
    echo ========================================
    echo.
    echo Please check the error messages above.
    echo.
    pause
)
