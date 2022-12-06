# Gunicorn configuration file

import os

bind = "0.0.0.0:5000"
workers = 2
reload = bool(int(os.getenv("GUNICORN_RELOAD", 1)))

# Logging configuration
accesslog = "-"
errorlog = "-"
