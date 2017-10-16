import sys

from pyramid.scripts.pserve import PServeCommand

from aarau.env import load_dotenv_vars


def main(argv=sys.argv, quiet=False):
    """Runs original pserve with .env support.
    """
    load_dotenv_vars()

    command = PServeCommand(argv, quiet=quiet)
    return command.run()


if __name__ == '__main__':
    sys.exit(main() or 0)
