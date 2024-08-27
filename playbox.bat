@echo off
powershell.exe -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

echo "Createing virtual environment..."
python -m venv venv

call venv/Scripts/activate

echo "Installing dependencies..."
pip install -r requirements.txt

:main

main.py
pause

goto main
