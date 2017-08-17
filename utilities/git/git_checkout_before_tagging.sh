#!/bin/bash

set -e
set -u


echo Checking out branch $GIT_FLOAT_BASE_BRANCH

# Checkout $GIT_FLOAT_BASE_BRANCH
git co $GIT_FLOAT_BASE_BRANCH

# Sanity check
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[
    ${CURRENT_BRANCH} != 'alpha'
    && ${CURRENT_BRANCH} != 'develop'
]]; then
    echo 'Please export $GIT_FLOAT_BASE_BRANCH to dev/alpha branch'
    exit 1
fi

