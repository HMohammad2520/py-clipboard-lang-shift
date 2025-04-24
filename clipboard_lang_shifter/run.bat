@echo off
setlocal

:: Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python.exe -m venv .venv

    :: Activate and install requirements
    echo Installing requirements...
    .\.venv\Scripts\python.exe -m pip install --upgrade pip
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
)

:: Run the application
echo Starting application...
.\.venv\Scripts\python.exe main.py

endlocal
