@echo off
echo Starting Doppler Inference Node...
echo Setting up Python environment...

:: Use the main Python installation that already has cryptography
C:\Users\amant\AppData\Local\Programs\Python\Python313\python.exe -m venv .venv

:: Activate and install requirements
call .venv\Scripts\activate.bat
pip install -r requirements.txt

:: Start the worker
echo.
echo Starting worker...
python worker.py
