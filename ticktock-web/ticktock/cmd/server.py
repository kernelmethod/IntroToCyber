# Handler for running the server subcommand

from ticktock.app import app

# admin = Admin(app, name="ticktock", template_mode="bootstrap3")


def server_handler(args):
    run_server(port=args.port, debug=args.debug)


def run_server(port: int = 5000, debug: bool = False):
    app.run(host="0.0.0.0", port=port, debug=debug)
