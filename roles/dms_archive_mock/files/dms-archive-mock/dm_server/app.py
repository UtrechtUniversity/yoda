from argparse import ArgumentParser
from .dm_server import MockServer
from flask import Flask
from flask import request

server = MockServer()
app = Flask(__name__)
BASEDIR = "/"


@app.route('/<path:path>', methods=['GET'])
def get_state(path):
    global server
    return server.get_state(path)


@app.route('/<path:path>', methods=['PUT'])
def put_state(path):
    global server
    remove = request.args.get('remove', default=0, type=int)
    op = request.args.get('op', default="put", type=str)
    if op == "put":
        server.put(path, remove)
    else:
        server.get(path)
    return server.get_state(path)


def run_app():
    global server
    parser = ArgumentParser(description='Process some integers.')
    parser.add_argument('--debug', action='store_true',
                        help='run in debug mode')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help='host of the service')
    parser.add_argument('--port', type=int, default=5000,
                        help='port of the service')
    parser.add_argument('--no_random_mig', action='store_false',
                        help='if set: do not randomize migration and unmigration times')
    parser.add_argument('--mig_time', type=int, default=10,
                        help='average migration time')
    parser.add_argument('--unmig_time', type=int, default=10,
                        help='average unmigration time')
    parser.add_argument('--basedir', type=str, default="/",
                        help='directory to be simulated (default /)')
    parser.add_argument('--allowed', type=str, nargs='*',
                        help=('list of allowed directories managed by the mock service.' +
                              'If list is empty, all directories under basedir (see --basedir) are allowed'))
    args = parser.parse_args()
    server.random_mig_time = args.no_random_mig
    server.default_mig_time = args.mig_time
    server.default_unmig_time = args.unmig_time
    server.basedir = args.basedir
    server.allowedlist = args.allowed
    app.run(debug=args.debug,
            host=args.host,
            port=args.port)


if __name__ == "__main__":
    run_app()
