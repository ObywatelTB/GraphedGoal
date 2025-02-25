#!/usr/bin/env python
"""
Script to start the FastAPI application.
This handles Python path issues to ensure proper module imports.
"""
import os
import sys
import uvicorn

# Add the parent directory to sys.path to ensure proper module resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(SCRIPT_DIR))

if __name__ == "__main__":
    # Run the app with the correct module path
    uvicorn.run("backend.app.main:app",
                host="0.0.0.0",
                port=8000,
                reload=True)
