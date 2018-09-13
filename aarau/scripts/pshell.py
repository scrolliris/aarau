import sys

from pyramid.scripts.pshell import PShellCommand

from aarau.env import load_dotenv_vars


def main(argv=None, quiet=False):
    """Runs original pshell with .env support."""
    if not argv:
        argv = sys.argv
    load_dotenv_vars()

    command = PShellCommand(argv, quiet=quiet)
    return command.run()


if __name__ == '__main__':
    sys.exit(main() or 0)
