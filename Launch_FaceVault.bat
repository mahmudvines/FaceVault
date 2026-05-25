@echo off
title FaceVault — Local Face Recognition
color 0B
cd /d "%~dp0"

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║         👁  FaceVault Launcher            ║
echo  ║   100%% offline face recognition app      ║
echo  ╚══════════════════════════════════════════╝
echo.

:: Try to find Python 3.11 or 3.12 in common locations
set PYTHON=
for %%P in (
    "py -3.11"
    "py -3.12"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "python3"
    "python"
) do (
    if not defined PYTHON (
        %%P --version >nul 2>&1
        if not errorlevel 1 set PYTHON=%%P
    )
)

if not defined PYTHON (
    echo  [ERROR] Python not found!
    echo.
    echo  Please install Python 3.11+ from:
    echo  https://www.python.org/downloads/
    echo  (tick "Add Python to PATH" during install)
    echo.
    pause
    exit /b 1
)

echo  [OK] Found Python: %PYTHON%
echo.
echo  Installing / checking dependencies...
echo.

%PYTHON% -m pip install flask pillow numpy tqdm --quiet --upgrade

echo.
echo  Checking face_recognition (may take a moment first time)...
%PYTHON% -c "import face_recognition" >nul 2>&1
if errorlevel 1 (
    echo  Installing face_recognition (this may take a few minutes)...
    %PYTHON% -m pip install face_recognition
)

echo.
echo  ══════════════════════════════════════════
echo   Starting FaceVault at http://localhost:5050
echo   Browser will open automatically.
echo   Close this window to stop the app.
echo  ══════════════════════════════════════════
echo.

%PYTHON% start.py

echo.
echo  FaceVault has stopped.
pause
