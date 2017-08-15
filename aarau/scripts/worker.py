import os
import sys

from pyramid.paster import setup_logging

from aarau.env import Env


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s \'development.ini#aarau\'")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv, quiet=False):
    if len(argv) < 2:
        usage(argv)

    Env.load_dotenv_vars()
    env = Env()

    config_uri = argv[1]
    setup_logging(config_uri)

    # default args
    loglevel = 'info'
    queues = 'default'

    if not env.is_production:
        loglevel = 'debug'

    os.system(
        'celery worker -A aarau.tasks.worker '
        '--ini {0!s} '
        '-E '
        '-l {1!s} '
        '-Q {2!s}'.format(config_uri, loglevel, queues))


if __name__ == '__main__':
    sys.exit(main() or 0)
