from slackbot.bot import respond_to, listen_to
from slackbot_settings import EVENT_URL
import json, requests
from dateutil import parser


def decode_event(events):
    ret = ''
    for event in events:
        time = parser.parse(event['start'])
        ret = ret + '%s: %s\n' %(event['summary'], time.strftime('%c'))
    return ret

@respond_to(r'^events$')
@respond_to(r'^events (.*)')
@listen_to(r'^events$')
@listen_to(r'^events (.*)')
def events(message, eventtype='extern'):
    string = requests.get(EVENT_URL)
    string.encoding = 'utf-8'
    events = json.loads(string.text)
    if eventtype == 'intern':
        message.reply(decode_event(events['intern']))
    else:
        message.reply(decode_event(events['public']))