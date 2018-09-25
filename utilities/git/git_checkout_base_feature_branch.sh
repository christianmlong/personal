#!/bin/bash

set -e
set -u


if ! [[ ${GIT_FLOAT_BASE_BRANCH} = STRY* ]]; then
    echo 'Please export GIT_FLOAT_BASE_BRANCH to a feature branch whose name starts with STRY'
    exit 1
fi

echo "Checking out feature branch $GIT_FLOAT_BASE_BRANCH"

# Checkout $GIT_FLOAT_BASE_BRANCH
git co "$GIT_FLOAT_BASE_BRANCH"

# Sanity check
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if ! [[ ${CURRENT_BRANCH} = STRY* ]]; then
    echo 'Please export GIT_FLOAT_BASE_BRANCH to a feature branch whose name starts with STRY'
    exit 1
fi

