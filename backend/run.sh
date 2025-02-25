#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI application
python main.py 