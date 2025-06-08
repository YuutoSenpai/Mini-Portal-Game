@echo off
REM Mini Portal Game Launcher for Windows
REM Activates virtual environment and runs the game

echo 🎮 Starting Mini Portal Game...

REM Activate virtual environment
call data\venv\Scripts\activate.bat

REM Run the game
python main.py

echo 👋 Thanks for playing!
pause