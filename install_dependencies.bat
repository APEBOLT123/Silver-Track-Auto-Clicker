@echo off
title Loading Silver Track Dependency Installer...
color 0A
echo =======================================================
echo       Loading Silver Track Dependency Installer...
echo =======================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b
)

REM Upgrade pip to the latest version
echo Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Failed to upgrade pip. Please check your Python installation.
    pause
    exit /b
)

REM Install required dependencies
echo Installing required dependencies...
pip install --force-reinstall pynput pyfiglet pillow
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Please check your internet connection.
    pause
    exit /b
)

echo.
echo =======================================================
echo       All dependencies installed successfully!
echo =======================================================
pause
exit /b
