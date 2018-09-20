import sys

from pyramid.scripts.pshell import PShellCommand
from webtest import TestApp

from aarau.env import load_dotenv_vars


def main(argv=None, quiet=False):
    """Runs original pshell with .env support."""
    if not argv:
        argv = sys.argv
    load_dotenv_vars()

    command = PShellCommand(argv, quiet=quiet)
    return command.run()


def setup(env):
    env['request'].host = 'example.org'
    env['request'].scheme = 'http'
    env['testapp'] = TestApp(env['app'])
    env['__'] = env['request'].localizer.translate
    env['db'] = env['request'].db


if __name__ == '__main__':
    sys.exit(main() or 0)
