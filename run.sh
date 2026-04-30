#!/bin/bash

# Personal Diary App - Run Script

echo ""
echo "======================================"
echo "     Personal Diary Web App"
echo "======================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Run the app
echo ""
echo "======================================"
echo "Starting Personal Diary App..."
echo "Open your browser to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "======================================"
echo ""

python app.py
