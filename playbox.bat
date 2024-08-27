@echo off
:: Set PowerShell execution policy
powershell.exe -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

:: Check if virtual environment exists
if not exist venv (
  echo Creating virtual environment...
  python -m venv venv
  
  :: Activate the virtual environment
  call venv\Scripts\activate

  :: Check if requirements.txt exists and install dependencies
  if exist requirements.txt (
    echo Installing dependencies...
    pip install -r requirements.txt
  ) else (
    echo requirements.txt is missing. Please provide requirements.txt and try again.
    exit /b 1
  )
) else (
  echo Virtual environment already exists.
)

:: Activate the virtual environment if it wasn't activated earlier
call venv\Scripts\activate

:: Run the Python script
python main.py

:: Wait for user input before closing
pause
