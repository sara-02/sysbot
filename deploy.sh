#!/usr/bin/env bash

# Travis build triggered on a forked repository
if [ "$TRAVIS_REPO_SLUG" != "systers/sysbot" ]; then
    echo "Skip publishing from forked repo."
    exit 0
fi

# Travis build triggered by a PR
if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
    echo "Skip publishing, just a PR."
    exit 0
fi

# Checking branch
if [ "$TRAVIS_BRANCH" == "develop" ]; then
    SERVER="sysbot-dev"
elif [ "$TRAVIS_BRANCH" == "master" ]; then
    SERVER="sysbot-prod"
else
    echo "Skip publishing, we don't publish for '$TRAVIS_BRANCH' branch"
    exit 0
fi

# Get the latest code
cd $HOME
git clone --branch=$TRAVIS_BRANCH https://github.com/systers/sysbot.git
cd sysbot

# Create AWS Elastic Beanstalk profile
mkdir ~/.aws
echo "[profile eb-cli]" > ~/.aws/config
echo "aws_access_key_id = $AWS_ACCESS_ID" >> ~/.aws/config
echo "aws_secret_access_key = $AWS_SECRET_KEY" >> ~/.aws/config

# Add environment variables
eb setenv USERNAME=$USERNAME
eb setenv PASSWORD=$PASSWORD
eb setenv path_secret=$path_secret
eb setenv api_key=$api_key
eb setenv BOT_ACCESS_TOKEN=$BOT_ACCESS_TOKEN
eb setenv legacy_token=$legacy_token

# Publishing
echo "Publishing to '$SERVER' server"
eb deploy
if [ $? -eq 0 ]; then
    echo "Publishing successful."
else
    echo "Publishing failed."
    exit 2
fi
