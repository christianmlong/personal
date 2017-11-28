#!/bin/bash

set -e
set -u

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo Auto-merge in to branch $GIT_FLOAT_BASE_BRANCH

if [[
    ${CURRENT_BRANCH} == 'alpha'
    || ${CURRENT_BRANCH} == 'stage'
    || ${CURRENT_BRANCH} == 'master'
    || ${CURRENT_BRANCH} == 'dev'
    || ${CURRENT_BRANCH} == 'develop'
]]; then
    echo "Please check out your feature branch first"
    exit 1
fi

# Merge the current branch to $GIT_FLOAT_BASE_BRANCH
git co $GIT_FLOAT_BASE_BRANCH
git merge --no-ff --no-edit $CURRENT_BRANCH
git branch -d $CURRENT_BRANCH
git push origin $GIT_FLOAT_BASE_BRANCH:$GIT_FLOAT_BASE_BRANCH
git float
