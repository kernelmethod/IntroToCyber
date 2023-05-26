# Handlers for database-related subcommands

from ticktock.app import app, db


def initdb(args):
    with app.app_context():
        db.create_all()


def destroydb(args):
    with app.app_context():
        db.drop_all()
