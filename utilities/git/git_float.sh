#!/bin/bash

set -e
set -u

# BASE_BRANCH=staging
BASE_BRANCH=development

git fetch --all --prune

git co $BASE_BRANCH
git up

git branch -f local_integration $BASE_BRANCH

for i in "$@"
do
    git co "$i"
    git rebase $BASE_BRANCH
done

git co local_integration

for i in "$@"
do
    # Print out some octopi
    printf '🐙  '
done
printf '\n'
git merge --no-edit "$@"

