import os
API_TOKEN = os.environ['SLACK_BOT_TOKEN']
DEFAULT_REPLY = "Try help!"

PLUGINS = [
    'slackbotjira',
    'plugins.sio.dagens',
    'plugins.help',
    'plugins.misc',
    'plugins.ruter.ruter',
    'plugins.in',
    'plugins.shodan.shodan',
    'plugins.garm'
]

#SLACKBOTJIRA
JIRA_URL = 'https://jira.cyb.no/'
JIRA_AUTH = (os.environ['JIRA_USER'], os.environ['JIRA_PASS'])
JIRA_PROJECTS = [
    'AG',
    'OKO',
    'XXX',
    'ESC',
    'HS',
    'PR',
    'RAP',
    'UT',
    'BAR',
    'IN',
    'KAFE'
]

#Event url
EVENT_URL = 'https://in.cyb.no/api/cal/upcoming'
INTERN_URL = 'https://in.cyb.no/api/'
