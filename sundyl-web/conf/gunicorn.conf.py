# Gunicorn configuration file

import os
from multiprocessing import cpu_count
from pathlib import Path

bind = "0.0.0.0:80"
workers = 2 * cpu_count() + 3
reload = bool(int(os.getenv("GUNICORN_RELOAD", 0)))
reload_extra = list((Path.cwd() / "sundyl" / "templates").glob("**/*.html"))

# Logging configuration
accesslog = "-"
errorlog = "-"
