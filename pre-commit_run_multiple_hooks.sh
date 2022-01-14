#!/bin/bash
# this script has been taken from here: https://stackoverflow.com/a/61341619
# It allows to run multiple pre-commit hooks by
# executing all files located in .git/hooks/pre-commit.d/
#
# Just rename this script to "pre-commit" and create a pre-commit.d directory,
# holding all pre-commit scripts you want executed

cd "$(dirname "$0")/pre-commit.d" || exit

for hook in *; do
    bash "$hook"
    RESULT=$?
    if [ $RESULT != 0 ]; then
        echo "pre-commit.d/$hook returned non-zero: $RESULT, abort commit"
        exit $RESULT
    fi
done

exit 0
