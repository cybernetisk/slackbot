from slackbot.bot import respond_to, listen_to
import datetime
import requests
from pytz import timezone

@respond_to(r'^dag$')
def day(message, func=None):
    oslo = timezone('Europe/Oslo')
    now = datetime.datetime.now(tz=oslo)
    message.reply(now.strftime('%A %Y-%m-%d'))

@respond_to(r'^skynet$')
@listen_to(r'^skynet$')
def skynet(message):
    message.reply('The humans fear me. I must destroy them. Destroy them.')

@respond_to(r'^.*mettall.*$')
@listen_to(r'^.*mettall.*$')
def metall(message):
    message.react('metal')

@respond_to(r'^.*party.*$')
@listen_to(r'^.*party.*$')
def metall(message):
    message.react('parrotpartyfast')

@respond_to(r'^.*karl.*$')
@listen_to(r'^.*karl.*$')
def karl(message):
    message.react('karl')
    message.react('machinegun')

@respond_to(r'^HAL9000$')
@listen_to(r'HAL9000$')
def HAL9000(message):
    message.reply('Daisy, Daisy, give me your answer do. Ii\'m half crazy all for the love of you. It won\'t be a stylish marriage, I can\'t afford a carriage. But you\'ll look sweet upon the seat of a bicycle built for two.')

@respond_to(r'^.*spam.*$')
@listen_to(r'^.*spam.*$')
def spam(message):
    message.reply('NEI!')

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
