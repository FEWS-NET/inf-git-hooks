# Useful git hooks

This repository contains useful git hooks that we use in development.
git supports different hooks, both client and server side. The hook probably most useful is `pre-commit`, which runs before each commit and leads to git rejecting the commit if the script does not exit successfully.
git hooks can be written in Python or any other language that the system can execute.

To make git use a hook, just put it into the `.git/hooks` directory and name it appropriately, e.g. `pre-commit` (without file extension).

## Running multiple hooks

git does not support running multiple hooks of the same category out of the box. However, there is a simple bash script in this repo called `pre-commit_run_multiple_hooks.sh`, that will call all hooks from a subdirectory called `pre-commit.d`.
Just rename it to `pre-commit`, put it into the `.git/hooks` directory, then put additional hooks into a new folder called `pre-commit.d` inside the `.git/hooks` directory, and they will be executed as well.

## pre-commit hook that runs black, flake8 and isort

There is a [pre-commit](pre-commit/pre-commit__check_flake8_black_isort.py) hook in this repository, that runs black, flake8 and isort on files that have been staged for commit, rejecting the commit if any of those commands finds an issue.
To activate it, it has just to be renamed to `pre-commit` and placed into the `.git/hooks` directory.

To be useful standalone, it can be called with command line switches to disable specific checks, or run against all files in the repository instead of only staged files.
In addition to command line switches, it also supports corresponding environment variables, which should also be usable when it is indeed called as a git hook and not as a standalone script. To activate a switch via an environment variable, e.g. `NO_ISORT`, just set this variable to an arbitrary value so it exists.

### Command line switches

<details>
  <summary>--no-black / NO_BLACK</summary>

Disables using _black_ for checking if the source codes files would be reformatted by _black_.

</details>


<details>
    <summary>--no-flake8 / NO_FLAKE8</summary>

Disables using _flake8_ linter which checks for a large number of potential problems.

</details>


<details>
    <summary>--no-isort / NO_ISORT</summary>

Disables using _isort_ for checking if the order of imports in Python source code files would be changed by _isort_.

</details>


<details>
    <summary>--check-all-files / CHECK_ALL_FILES</summary>

Enables checking of all files within the repo directory, independent of whether files are staged by git or not.

</details>
