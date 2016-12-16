from slackbot.bot import respond_to, listen_to
import datetime
import requests
from pytz import timezone

@respond_to(r'^dag$')
def day(message, func=None):
    oslo = timezone('Europe/Oslo')
    now = datetime.datetime.now(tz=oslo)
    message.reply(now.strftime('%A %Y-%m-%d'))


@respond_to(r'^ping$')
@listen_to(r'^!ping$')
def ping(message):
    message.reply('Pong!')

@respond_to(r'^commit$')
@listen_to(r'^!commit$')
def commit(message):
    url = "http://whatthecommit.com/index.txt"
    commitmessage = requests.get(url).text
    message.reply(commitmessage)

@respond_to(r'^repo$')
@listen_to(r'^!repo$')
def repo(message):
    message.reply('https://github.com/cybrairai/slackbot')