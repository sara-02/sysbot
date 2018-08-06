#!/usr/bin/env bash

# Travis build triggered on a forked repository
if [ "$TRAVIS_REPO_SLUG" != "systers/sysbot" ]; then
    echo "Skip tests running from forked repo."
    exit 0
fi

# Travis build triggered by a PR
if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
    echo "Run tests only once( for the push )."
    exit 0
fi

coverage run --source code -m unittest discover tests
coverage report -m
