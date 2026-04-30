@echo off
REM Personal Diary App - Run Script

echo.
echo ======================================
echo     Personal Diary Web App
echo ======================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt -q

REM Run the app
echo.
echo ======================================
echo Starting Personal Diary App...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ======================================
echo.

python app.py

pause
