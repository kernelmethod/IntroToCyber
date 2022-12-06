# Handlers for database-related subcommands

from ticktock.app import db


def initdb(args):
    db.create_all()


def destroydb(args):
    db.drop_all()
