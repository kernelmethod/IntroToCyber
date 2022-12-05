from .app import app
from .notice import Notice, NoticeLevel  # noqa: F401

from ticktock.api import api
from ticktock.feed import feed
from ticktock.logging import setup_logger, getLogger  # noqa: F401
from ticktock.login import login_manager, auth

login_manager.init_app(app)
app.register_blueprint(api)
app.register_blueprint(auth)
app.register_blueprint(feed)
