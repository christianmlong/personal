#!/bin/bash

set -e
set -u

CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD`
INTEGRATION_BRANCH=local_integration

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
git up

git branch -f $INTEGRATION_BRANCH $GIT_FLOAT_BASE_BRANCH

for i in "$@"
do
    git co "$i"
    git rebase $GIT_FLOAT_BASE_BRANCH
done

git co $INTEGRATION_BRANCH

for i in "$@"
do
    # Print out some octopi
    printf '🐙  '
done
printf '\n'
git merge --no-edit "$@"

git co $CURRENT_BRANCH
