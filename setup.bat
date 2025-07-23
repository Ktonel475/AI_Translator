@echo off
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Running Initialization...
python setup.py

pause
