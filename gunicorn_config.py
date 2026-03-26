# gunicorn_config.py
import os
import sys

# Create logs directory if it doesn't exist (only if we must use file logs)
LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(LOGS_DIR):
    try:
        os.makedirs(LOGS_DIR)
    except:
        # If we can't create the directory, fall back to stdout
        pass

# Server socket
bind = "0.0.0.0:8000"

# Worker processes
workers = 1
worker_class = "sync"
timeout = 120

# Logging - try file logs first, fall back to stdout
try:
    accesslog = os.path.join(LOGS_DIR, "access.log") if os.path.exists(LOGS_DIR) else "-"
    errorlog = os.path.join(LOGS_DIR, "error.log") if os.path.exists(LOGS_DIR) else "-"
except:
    accesslog = "-"
    errorlog = "-"

loglevel = "info"

# Disable file logging completely - just use stdout
accesslog = "-"
errorlog = "-"

# Other settings
preload_app = True