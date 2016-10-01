import os
API_TOKEN = os.environ['SLACK_BOT_TOKEN']
DEFAULT_REPLY = "Try help!"

PLUGINS = [
    'slackbotjira',
    'plugins.dagens',
    'plugins.help',
    'plugins.misc',
    'plugins.ruter'
]

#SLACKBOTJIRA
JIRA_URL = 'https://jira.cyb.no/'
JIRA_AUTH = (os.environ['JIRA_USER'], os.environ['JIRA_PASS'])
JIRA_PROJECTS = ['AG', 'CYBOKO', 'DRIFT', 'ESC', 'HS', 'PR' 'RAP','UT']