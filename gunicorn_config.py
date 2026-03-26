# gunicorn_config.py
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# Process naming
proc_name = "kjc-website"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if using HTTPS)
# keyfile = "/path/to/ssl/key.pem"
# certfile = "/path/to/ssl/cert.pem"

# For production, set these environment variables
raw_env = [
    'FLASK_ENV=production',
    'SECRET_KEY=your-secret-key-change-this-in-production',
]

# Preload app for better performance
preload_app = True

# Graceful timeout
graceful_timeout = 30

# Maximum requests before worker restart
max_requests = 1000
max_requests_jitter = 50