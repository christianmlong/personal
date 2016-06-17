#!/bin/bash

set -e
set -u

CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD`
INTEGRATION_BRANCH=local_integration

if [ $# -eq 0 ]; then
    echo "Please provide at least one branch name"
    exit 1
fi

DO_MERGE=true
DO_PULL_UPSTREAM=true
# Note: The way this is written, you can't supply both --no-merge and
# --no-pull-upstream options. If that becomes necessary, then we might look at
# rewriting this in Python.
if [ "$1" = "--no-merge" ]; then
    DO_MERGE=false
    shift
elif [ "$1" = "--no-pull-upstream" ]; then
    DO_PULL_UPSTREAM=false
    shift
fi

if [ $# -eq 0 ]; then
    echo "Please provide at least one branch name"
    exit 1
fi

if [ $CURRENT_BRANCH == $INTEGRATION_BRANCH ]; then
    echo "You are on branch ${CURRENT_BRANCH}. Switch to a feature branch before running"
    exit 1
fi

echo Float on top of $GIT_FLOAT_BASE_BRANCH

git fetch --all --prune

git co $GIT_FLOAT_BASE_BRANCH

if [ "$DO_PULL_UPSTREAM" = "true" ]; then
    git up
fi

git branch -f $INTEGRATION_BRANCH $GIT_FLOAT_BASE_BRANCH

for i in "$@"
do
    git co "$i"
    git rebase $GIT_FLOAT_BASE_BRANCH
done

git co $INTEGRATION_BRANCH

if [ "$DO_MERGE" = "true" ]; then
    for i in "$@"
    do
        # Print out some octopi
        printf '🐙  '
    done
    printf '\n'

    git merge --no-ff --no-edit "$@"
fi

git co $CURRENT_BRANCH
