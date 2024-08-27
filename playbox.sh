#!/bin/bash

# Set up the Python virtual environment and install dependencies

# Check if virtual environment exists
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv

  # Activate the virtual environment
  source venv/bin/activate

  # Check if requirements.txt exists and install dependencies
  if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
  else
    echo "requirements.txt is missing. Please provide requirements.txt and try again."
    exit 1
  fi
else
  echo "Virtual environment already exists."
  # Activate the virtual environment if it exists
  source venv/bin/activate
fi

# Run the Python script
python3 main.py

# Pause to keep the terminal open (for interactive sessions)
read -p "Press [Enter] key to exit..."
