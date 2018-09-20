import sys

from pyramid.scripts.proutes import PRoutesCommand

from aarau.env import load_dotenv_vars


def main(argv=None, quiet=False):
    """Runs original proutes with .env support."""
    if not argv:
        argv = sys.argv
    load_dotenv_vars()

    command = PRoutesCommand(argv, quiet=quiet)
    return command.run()


if __name__ == '__main__':
    sys.exit(main() or 0)
