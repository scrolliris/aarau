import os
import sys

from pyramid.paster import (
    get_app,
    setup_logging
)

from aarau.env import Env, load_dotenv_vars


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s {development|production}.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=None):
    if not argv:
        argv = sys.argv

    if len(argv) < 2:
        usage(argv)

    load_dotenv_vars()
    env = Env()

    config_uri = argv[1]
    wsgi_app = get_app(config_uri)
    setup_logging(config_uri)

    from paste.script.cherrypy_server import cpwsgi_server
    cpwsgi_server(wsgi_app, host=env.host, port=env.port,
                  numthreads=10, request_queue_size=100)


if __name__ == '__main__':
    sys.exit(main() or 0)
