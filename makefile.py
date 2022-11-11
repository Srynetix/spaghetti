import sys

import click
from duct import Expression, cmd


@click.group()
def run() -> None:
    """Makefile entry-point."""


def _run_and_die_if_error(cmd: Expression) -> None:
    output = cmd.unchecked().run().status
    if output != 0:
        sys.exit(output)


@click.command(help="format code")
def fmt() -> None:
    cmd("isort", ".").run()
    cmd("black", ".").run()


@click.command(help="lint code")
def lint() -> None:
    _run_lint()


@click.command(help="test code")
def test() -> None:
    _run_tests()


@click.command(help="run CI checks")
def ci() -> None:
    _run_lint()
    _run_tests()


def _run_lint() -> None:
    _run_and_die_if_error(cmd("black", "--check", "."))
    _run_and_die_if_error(cmd("flakeheaven", "lint"))
    _run_and_die_if_error(cmd("mypy", "--strict", "."))


def _run_tests() -> None:
    _run_and_die_if_error(cmd("pytest", "-vv", "tests", "--cov=."))


run.add_command(fmt)
run.add_command(lint)
run.add_command(test)
run.add_command(ci)

if __name__ == "__main__":
    run()
