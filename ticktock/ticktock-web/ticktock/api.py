# Source for the TickTock API

import flask
import flask_login
from flask import request
from sqlalchemy import exc
from ticktock import forms, logging, Notice
from ticktock.app import csrf, db
from ticktock.logging import getLogger
from ticktock.model import Post, User

api = flask.Blueprint("api", __name__, url_prefix="/api")


@api.route("/user", methods=["GET"])
def user_api_info():
    return {
        "message": f"Usage: GET {flask.request.path}/<user_id>",
    }


@api.route("/user/<int:uid>", methods=["GET"])
def get_user(uid: int):
    """Fetch the user with the given UID."""

    if (user := User.query.filter_by(uid=uid).first()) is None:
        return {"error": f"User with UID {uid} not found"}, 404

    # The path to the user's avatar can automatically be crafted from their
    # username and user ID
    return {
        "username": user.username,
        "uid": uid,
        "avatar": f"/s3/avatar/{uid}",
    }


@api.route("/search", methods=["GET"])
@csrf.exempt
def search():
    """Search posts matching some regex."""
    logger = logging.getLogger()
    form = forms.SearchForm(meta={"csrf": False})
    posts = []

    if (query := request.args.get("query")) is not None:
        # Pre-populate searchbar with last query
        form.query.data = query
        logger.info("Received query: %s", repr(query))

    if form.validate() and query is not None:
        # Try to search for posts containing the input text. The following query
        # searches for a regular expression in Postgres.
        # NOTE: intentionally vulnerable to SQLi!
        sql = (
            "SELECT u.username, u.uid, p.content, p.posted, p.post_id "
            "FROM posts p INNER JOIN users u "
            "ON u.uid = p.author_id "
            f"WHERE p.content ~ '{query}'"
        )

        posts = list(db.engine.execute(sql))
        logger.debug("result = %s", repr(posts))

    # Return search results as JSON
    fields = ("username", "uid", "content", "posted", "post_id")
    posts = [dict(zip(fields, p)) for p in posts]
    return {"results": posts}


@api.route("/posts/recent", methods=["GET"])
def get_recent():
    """Get the most recent posts."""

    posts = Post.query.order_by(Post.posted.desc()).limit(50).all()
    return {"posts": [p.to_json() for p in posts]}


@api.route("/posts/id/<int:post_id>", methods=["GET"])
def get_post_by_id(post_id: int):
    """Get the post with the given ID."""

    post = Post.query.filter_by(post_id=post_id).first()

    if post is None:
        result = {"error": f"Post {post_id} not found"}
        return result, 404

    return post.to_json()


@api.route("/posts/user/<int:uid>", methods=["GET"])
def get_post_by_user(uid: int):
    """Get posts from the given user."""

    posts = Post.query.filter_by(author_id=uid).all()
    return {"posts": [p.to_json() for p in posts]}


@api.route("/posts/create", methods=["POST"])
@flask_login.login_required
def create_post():
    """Create a new post."""

    form = forms.PostForm()
    kwargs = {}

    uid = flask_login.current_user.uid
    getLogger().debug("flask_login.current_user = %s", repr(flask_login.current_user))

    try:
        if form.validate_on_submit():
            post = Post(author_id=uid, content=form.content.data)
            db.session.add(post)
            db.session.commit()
        else:
            kwargs["notice"] = Notice("Error submitting message")

    except exc.IntegrityError:
        kwargs["notice"] = Notice("Database error")

    return flask.redirect("/", **kwargs)
