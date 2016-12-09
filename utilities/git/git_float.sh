#!/bin/bash

set -e
set -u

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
INTEGRATION_BRANCH=local_integration

DO_MERGE=false
DO_PULL_UPSTREAM=true
# Note: The way this is written, you can't supply both --merge and
# --no-pull-upstream options. If that becomes necessary, then we might look at
# rewriting this in Python.
if [ "$1" = "--merge" ]; then
    DO_MERGE=true
    shift
elif [ "$1" = "--no-pull-upstream" ]; then
    DO_PULL_UPSTREAM=false
    shift
elif [[ "$1" == --* ]]; then
    echo "Unrecognized argument ${1}"
    exit 1
fi

if [ $# -eq 0 ]; then
    BRANCHES=$(git branch --no-merge)
else
    # Here we are taking all of the arguments from the
    # command line. We used to use "$@", and handle them
    # as an array, but for parallelism with the other branch
    # of this if statement, I'm handling them as one string
    # now.
    # Reference
    # http://stackoverflow.com/questions/3008695/what-is-the-difference-between-and-in-bash
    BRANCHES="$*"
fi

# Here's how to handle BRANCHES as an array instead of as a
# whitespace-delimited string. However, you would have to change things like
# this
#    git merge --no-ff --no-edit "$BRANCHES"
# so that they worked on the whole list of branches, not just
# the first element.
#
# declare -a BRANCHES
# if [ $# -eq 0 ]; then
#     # Make an array
#     read -r -a BRANCHES <<< "$(git branch --no-merge)"
# else
#     # Read the arguments as an array
#     BRANCHES=("$@")
# fi

if [ "$CURRENT_BRANCH" == "$INTEGRATION_BRANCH" ]; then
    echo "You are on branch ${CURRENT_BRANCH}. Switch to a feature branch before running"
    exit 1
fi

echo "Float on top of $GIT_FLOAT_BASE_BRANCH"

git fetch --all --prune

git co "$GIT_FLOAT_BASE_BRANCH"

if [ "$DO_PULL_UPSTREAM" = "true" ]; then
    git up
fi

git branch -f "$INTEGRATION_BRANCH" "$GIT_FLOAT_BASE_BRANCH"

# Here we're iterating over a space-delimited string or a newline-delimited
# string Since IFS is at its default value of (space, tab, newline), this
# works. The alternative would be to make BRANCHES be an array variable.
for i in $BRANCHES
do
    git co "$i"
    git rebase "$GIT_FLOAT_BASE_BRANCH"
done

git co "$INTEGRATION_BRANCH"

if [ "$DO_MERGE" = "true" ]; then
    for i in $BRANCHES
    do
        # Print out some octopi
        printf '🐙  '
    done
    printf '\n'

    git merge --no-ff --no-edit "$BRANCHES"
fi

git co "$CURRENT_BRANCH"
