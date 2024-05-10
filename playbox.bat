@echo off
powershell.exe -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

python -m venv venv

call venv/Scripts/activate

pip install -r requirements.txt

:main

main.py
pause

goto main