@echo off
setlocal

echo.
echo =================================================
echo      Preparing system for Auto Subtitles Generator
echo =================================================
echo.

:: 1. Check for Docker
echo [1/5] Checking for Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [X] Error: Docker is not installed or the Docker daemon is not running.
    echo   Please install Docker Desktop and ensure it's running.
    echo   Download from: https://www.docker.com/products/docker-desktop/
    goto :error
) else (
    echo   [+] Docker is installed.
)
echo.

:: 2. Check for Python 3.12+ (Robust Method)
echo [2/5] Checking for Python 3.12 or newer...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [X] Error: Python is not installed or not found in PATH.
    goto :python_error
)

:: Directly check the output of python --version for required versions
python --version 2>&1 | findstr /C:" 3.12" /C:" 3.13" /C:" 3.14" /C:" 3.15" >nul
if %errorlevel% neq 0 (
    echo   [X] Error: Python version 3.12 or newer is required.
    echo   Please run 'python --version' to see your current version.
    goto :python_error
) else (
    echo   [+] Compatible Python version found.
)
echo.


:: 3. Set up virtual environment using virtualenv
echo [3/5] Setting up Python virtual environment...
:: Check if virtualenv is installed, and install it if not
pip install virtualenv >nul
if %errorlevel% neq 0 (
    echo   [-] 'virtualenv' package not found. Installing it now...
    py -m pip install virtualenv
    if %errorlevel% neq 0 (
        echo   [X] Failed to install 'virtualenv'. Please check your pip configuration.
        goto :error
    )
) else (
    echo   [+] 'virtualenv' package is already installed.
)

if not exist venv (
    echo   [-] Creating virtual environment in 'venv' folder using virtualenv...
    virtualenv venv
    if %errorlevel% neq 0 (
        echo   [X] The command to create the virtual environment failed.
        goto :error
    )
) else (
    echo   [+] Virtual environment folder already exists.
)

:: Verify that the virtual environment was created correctly
if not exist venv\Scripts\activate.bat (
    echo   [X] CRITICAL ERROR: The virtual environment was not created correctly.
    echo   The 'venv\Scripts\activate.bat' file is missing.
    echo   This usually indicates a problem with the Python installation or virtualenv.
    echo   Please try reinstalling Python, ensuring all standard features are included.
    goto :error
)

echo   [-] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

:: 4. Check for Tkinter and install requirements
echo [4/5] Installing Python packages...
:: Check if Tkinter is available
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo   [X] Error: Tkinter module not found.
    echo   Please reinstall Python and make sure to include "tcl/tk and IDLE".
    goto :error
) else (
    echo   [+] Tkinter module is available.
)

echo   [-] Upgrading pip...
python -m pip install --upgrade pip >nul
echo   [-] Installing packages from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo   [X] Failed to install Python packages. Check your internet connection.
    goto :error
)
echo   [+] Python packages installed successfully.
echo.

:: 5. Check for VLC
echo [5/5] Checking for VLC Media Player...
echo   [!] IMPORTANT: This script cannot automatically verify if VLC is installed.
echo   Please ensure you have VLC Media Player on your system for the video player to work.
echo   Download from: https://www.videolan.org/
echo.

echo =================================================
echo      ✅ System ready!
echo =================================================
echo.
echo The virtual environment is active in this terminal.
echo To run the application, execute: python main.py
echo.
goto :end

:python_error
echo   Please install Python 3.12+ from python.org.
echo   IMPORTANT: During installation, make sure to check the box "Add python.exe to PATH".
goto :error

:error
echo.
echo =================================================
echo      ❌ Setup failed.
echo =================================================
echo Please fix the errors above and run the script again.

:end
pause
endlocal