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
    _run_and_die_if_error(cmd("black", "--check", "."))
    _run_and_die_if_error(cmd("flakeheaven", "lint"))


run.add_command(fmt)
run.add_command(lint)

if __name__ == "__main__":
    run()
