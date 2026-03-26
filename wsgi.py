# wsgi.py
import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Import your Flask app
from app import app as application

# For PythonAnywhere, you might need this
if __name__ == "__main__":
    application.run()