# Flask blueprint for the post feed

import flask
import flask_login
from flask import request, url_for
from ticktock.logging import getLogger
from ticktock.forms import PostForm, SearchForm
from ticktock.model import Post, User
from ticktock.utils import render_template

feed = flask.Blueprint("feed", __name__, url_prefix="/")


@feed.route("/", methods=["GET"])
def index():
    getLogger().debug("flask_login.current_user = %S", repr(flask_login.current_user))
    form = PostForm()
    return render_template("index.html", form=form)


@feed.route("/post", methods=["GET"])
def get_post():
    # Post ID must be specified, otherwise the user should be redirected
    # to the homepage
    if (post_id := request.args.get("id")) is None:
        return flask.redirect(url_for("feed.index"))

    post = Post.query.filter_by(post_id=post_id).first()
    if post is None:
        return render_template("post.html"), 404

    kwargs = {
        "username": post.author.username,
        "uid": post.author_id,
        "content": post.content,
        "posted": post.posted,
        "post_id": post.post_id,
    }

    # Try to find the post with the given ID
    # post = Post.query.filter_by(post_id=post_id).first()
    return render_template("post.html", **kwargs)


@feed.route("/user/<username>", methods=["GET"])
def get_user_posts(username: str):
    if (user := User.query.filter_by(username=username).first()) is None:
        return render_template("user.html", uid=None), 404

    return render_template("user.html", uid=user.uid, username=user.username)


@feed.route("/search", methods=["GET"])
def search():
    """Show search page to user."""

    form = SearchForm()
    if (query := request.args.get("query")) is not None:
        form.query.data = query

    return render_template("search.html", form=form)
