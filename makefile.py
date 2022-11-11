import sys

import click
from duct import cmd


@click.group()
def run():
    """Makefile entry-point."""


def _run_and_die_if_error(cmd):
    output = cmd.unchecked().run().status
    if output != 0:
        sys.exit(output)


@click.command(help="format code")
def fmt():
    cmd("isort", ".").run()
    cmd("black", ".").run()


@click.command(help="lint code")
def lint():
    _run_lint()


@click.command(help="test code")
def test():
    _run_tests()


@click.command(help="run CI checks")
def ci():
    _run_lint()
    _run_tests()


def _run_lint():
    _run_and_die_if_error(cmd("black", "--check", "."))
    _run_and_die_if_error(cmd("flakeheaven", "lint"))


def _run_tests():
    _run_and_die_if_error(cmd("pytest", "-vv", "tests", "--cov=."))


run.add_command(fmt)
run.add_command(lint)
run.add_command(test)
run.add_command(ci)

if __name__ == "__main__":
    run()
