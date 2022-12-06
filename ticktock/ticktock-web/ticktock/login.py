import flask
import flask_login
import random
import typing as _t
from sqlalchemy import exc, func
from ticktock import Notice, config
from ticktock.app import csrf, db
from ticktock.logging import getLogger
from ticktock.forms import AuthForm, LogoutForm
from ticktock.model import User
from ticktock.utils import change_avatar, render_template

login_manager = flask_login.LoginManager()
auth = flask.Blueprint("auth", __name__, url_prefix="/")


@login_manager.user_loader
def user_loader(uid: str) -> _t.Optional[User]:
    try:
        uid = int(uid)
    except ValueError:
        return None

    return User.query.filter_by(uid=uid).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get("username")
    return User.query.filter_by(username=username).first()


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = AuthForm()
    kwargs = {
        "auth_switch_url": flask.url_for("auth.signup"),
        "action": "login",
        "form": form,
    }

    if flask.request.method == "GET":
        # Render the login view
        return render_template("login.html", **kwargs)

    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data, password=form.password.data
        ).first()

        getLogger().info(f"{user = }")

        if user is not None:
            flask_login.login_user(user)
            getLogger().info("Logged in user %s", user.username)
            flask.flash("Login successful!")
            return flask.redirect("/")

    notice = Notice.error("Unable to login")
    return render_template("login.html", banner_notice=notice, **kwargs), 400


@auth.route("/logout", methods=["POST"])
@flask_login.login_required
@csrf.exempt
def logout():
    """Logout endpoint.

    NOTE: CSRF protection is explicitly disabled from this endpoint for demonstration/lab
    purposes!
    """
    form = LogoutForm(meta={"csrf": False})

    if form.validate_on_submit():
        flask_login.logout_user()

    return flask.redirect("/")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = AuthForm()
    kwargs = {
        "auth_switch_url": flask.url_for("auth.login"),
        "action": "signup",
        "form": form,
    }

    if flask.request.method == "GET":
        return render_template("signup.html", **kwargs)

    notice = None

    try:
        if form.validate_on_submit():
            # Attempt to create a new user with the given username and password
            uid = db.session.query(func.max(User.uid)).scalar() + 1
            user = User(username=form.username.data, password=form.password.data, uid=uid)
            db.session.add(user)
            db.session.commit()

            getLogger().info("Added new user %s", form.username.data)

            # Use a random profile image for the user
            imgs = list(config.misc_img.glob("profile_default_*"))
            img = random.choice(imgs)
            change_avatar(uid, img)

            # Login as the new user
            user = User.query.filter_by(username=form.username.data).first()
            flask_login.login_user(user)
            return flask.redirect("/")

        notice = Notice.error("Unable to sign up")

    except exc.IntegrityError:
        notice = Notice.error("Database integrity error")
        db.session.rollback()

    if notice is None:
        notice = Notice.error("Unable to sign up")

    kwargs["form"] = AuthForm(meta={"csrf": False})
    return render_template("signup.html", banner_notice=notice, **kwargs), 400
