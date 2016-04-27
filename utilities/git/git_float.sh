#!/bin/bash

# BASE_BRANCH=staging
BASE_BRANCH=development

# Array of branch names
declare -a branches=(
    "personal"
    "hiera_warning"
)

git fetch --all --prune

git co $BASE_BRANCH
git up

git branch -f local_integration $BASE_BRANCH

for i in "${branches[@]}"
do
    git co "$i"
    git rebase $BASE_BRANCH
done

git co local_integration

if [ "$1" == "--standard" ]; then
    for i in "${branches[@]}"
    do
        git merge --no-edit "$i"
    done
else
    for i in "${branches[@]}"
    do
        # Print out some octopi
        printf '🐙  '
    done
    printf '\n'
    git merge --no-edit "${branches[@]}"
fi

