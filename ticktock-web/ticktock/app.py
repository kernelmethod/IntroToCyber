import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from secrets import token_hex
from ticktock import config
from ticktock.logging import setup_logger, getLogger
from ticktock.utils import render_template

app = Flask(
    __name__,
    template_folder=config.template_folder,
    static_folder=config.static_folder,
)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", token_hex(32))
app.config["SQLALCHEMY_DATABASE_URI"] = config.db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = bool(int(os.getenv("SQLALCHEMY_ECHO", 0)))
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

setup_logger(level=logging.INFO)

if (flag := os.getenv("DIRECTORY_ENUMERATION_FLAG")) is not None:
    getLogger().debug("Adding DIRECTORY_ENUMERATION_FLAG")

    @app.route("/pressreleases")
    def enumeration_flag():
        """Custom route for the directory enumeration flag."""
        return render_template("direnum_flag.html", flag=flag)
