#!/usr/bin/env python
"""git pre-commit hook that will reject commits with unformatted .py files.

We could let black check the whole source code, but to allow incremental updating of
unformatted files we will only reject unformatted files that are staged for commit.
"""
import argparse
import os
import shlex
import subprocess  # noqa: S404
import sys


def get_files_to_check() -> list[str]:
    # calling git diff to identify the files which are staged for commit
    # check_output returns a bytestring, so we have to decode to str
    git_cmd_return = subprocess.run(  # noqa: S603
        shlex.split("git diff --cached --name-only"),
        stdout=subprocess.PIPE,
        encoding="UTF-8",
    )
    files_to_check = [
        path
        for path in git_cmd_return.stdout.splitlines()
        if
        # only process files that exist, otherwise black will fail
        # when we delete a .py file
        path.endswith(".py") and os.path.exists(path)
    ]
    return files_to_check


def run_cmd(cmd: list[str]) -> None:
    try:
        subprocess.run(  # noqa: S603
            cmd, check=True, stderr=subprocess.PIPE, encoding="UTF-8"
        )
    except subprocess.CalledProcessError as exc:
        sys.exit(
            (
                f"{cmd[0]} check failed. Commit rejected, you have to "
                f"fix the {cmd[0]} violations first.\n{exc.stderr}"
            )
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="pre-commit hook to check for flake8, black, isort."
    )
    parser.add_argument(
        "--black",
        default=False if "NO_BLACK" in os.environ else True,
        action=argparse.BooleanOptionalAction,
        help="Whether to run black on changed files (default=True).",
    )
    parser.add_argument(
        "--flake8",
        default=False if "NO_FLAKE8" in os.environ else True,
        action=argparse.BooleanOptionalAction,
        help="Whether to run flake8 on changed files (default=True).",
    )
    parser.add_argument(
        "--isort",
        default=False if "NO_ISORT" in os.environ else True,
        action=argparse.BooleanOptionalAction,
        help="Whether to run isort on changed files (default=True).",
    )
    parser.add_argument(
        "--check-all-files",
        default="CHECK_ALL_FILES" in os.environ,
        action=argparse.BooleanOptionalAction,
        help="Whether to run checks on all files (instead of only staged files)",
    )

    parsed_args = parser.parse_args()

    files_to_check = ["."] if parsed_args.check_all_files else get_files_to_check()
    if not files_to_check:
        sys.exit()

    checks = ["black", "flake8", "isort"]
    cmd_extras = {"black": ["--check"], "isort": ["--check"]}

    cmds = []

    for check in checks:
        if getattr(parsed_args, check) is True:
            cmd = [check] + cmd_extras.get(check, []) + files_to_check
            cmds.append(cmd)

    for cmd in cmds:
        run_cmd(cmd)
