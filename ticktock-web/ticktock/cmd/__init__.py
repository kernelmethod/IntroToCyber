# Handlers for different subcommands

import argparse
from .db import initdb, destroydb
from .server import server_handler
from .server import run_server  # noqa: F401
from . import generate

argparser = argparse.ArgumentParser(
    prog="ticktock",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
argparser.add_argument(
    "--debug",
    action="store_true",
    help="Enable debug logging and run the Flask app in development mode",
)

subparsers = argparser.add_subparsers(title="subcommand")

server_parser = subparsers.add_parser("server", help="Run the web server")
server_parser.set_defaults(func=server_handler)
server_parser.add_argument(
    "-p",
    "--port",
    type=int,
    default="5000",
    help="The port that the server should listen on",
)

generate.add_subcommands(subparsers)

initdb_parser = subparsers.add_parser("initdb", help="Initialize the database")
initdb_parser.set_defaults(func=initdb)

destroydb_parser = subparsers.add_parser("destroydb", help="Drop all tables from the database")
destroydb_parser.set_defaults(func=destroydb)
