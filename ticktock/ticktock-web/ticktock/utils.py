import flask
import functools
import magic
import os
from minio import Minio
from pathlib import Path
from ticktock import config, forms


def change_avatar(uid: int, img: Path):
    mime = magic.from_file(img, mime=True)
    client = Minio(
        "s3.ticktock.lab:9000",
        access_key=os.environ["MINIO_ROOT_USER"],
        secret_key=os.environ["MINIO_ROOT_PASSWORD"],
        secure=False,
    )
    client.fput_object(config.buckets["avatar"], str(uid), img, content_type=mime)


@functools.wraps(flask.render_template)
def render_template(*args, **kwargs):
    """Custom version of ``flask.render_template`` that automatically defines some
    variables used by views of the site."""

    return flask.render_template(*args, logout_form=forms.LogoutForm(), **kwargs)
