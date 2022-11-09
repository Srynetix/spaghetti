import sys

from duct import cmd


def _run_and_die_if_error(cmd):
    output = cmd.unchecked().run().status
    if output != 0:
        sys.exit(output)


def format():
    cmd("isort", ".").run()
    cmd("black", ".").run()


def lint():
    _run_and_die_if_error(cmd("black", "--check", "."))
    _run_and_die_if_error(cmd("flakeheaven", "lint"))
