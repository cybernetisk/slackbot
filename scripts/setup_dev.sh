#!/bin/bash

set -e

VIRTUALENV=slackbot
VIRTUALENVACT=~/.virtualenvs/$VIRTUALENV/bin/activate

jira_user_file=config/jira-user.txt
jira_pass_file=config/jira-pass.txt
slack_token_file=config/slack-api-token.txt

#Deactivate vitualenv
deativate 2>/dev/null || true

#Make the config folder if it doesn't exist
if ! [ -d "config/" ]; then
mkdir config
fi

#JIRA credentials
if ! [ -f "$jira_user_file" ]; then
printf "Enter your jira user: "
read -s jira_user
echo 'Saving username to use later'
echo "$jira_user" >$jira_user_file
fi

if ! [ -f "$jira_pass_file" ]; then
printf "Enter your jira password: "
read -s jira_pass
echo 'Saving your password for later'
echo "$jira_pass" >$jira_pass_file
fi

#Setting up the SLACK token
if ! [ -f "$slack_token_file" ]; then
printf "Enter your a slack api token: "
read -s slack_token
echo 'Saving username to use later'
echo "$slack_token" >$slack_token_file
fi

#Install python, pip, virtualenv
sudo apt-get install python3 python3-pip virtualenv virtualenvwrapper

#setup virtualenv
# Set up virtualenv for Python
# This will let us install Python-packages for this project only
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
mkvirtualenv -p /usr/bin/python3 $VIRTUALENV || true

if [ ! -f "$VIRTUALENVACT" ]; then
    echo "Setup of virtualenv failed, cannot find installation"
    exit 1
fi

# Activate the virtual environment
workon $VIRTUALENV

#Setup variables
export SLACK_BOT_TOKEN=$(<$slack_token_file)
export JIRA_USER=$(<$jira_user_file)
export JIRA_PASS=$(<$jira_pass_file)

#Install requirements
pip install -r requirements.txt

#start bot
python run.py