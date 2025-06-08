#!/bin/bash
# Mini Portal Game Launcher
# Activates virtual environment and runs the game

# Get the script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "🎮 Starting Mini Portal Game..."

# Activate virtual environment
source "$DIR/data/venv/bin/activate"

# Run the game
python "$DIR/main.py"

echo "👋 Thanks for playing!"