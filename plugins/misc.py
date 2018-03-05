import datetime

import requests
from pytz import timezone
from slackbot.bot import respond_to, listen_to
from api import CybApi

@respond_to(r'^dag$')
def day(message, func=None):
    oslo = timezone('Europe/Oslo')
    now = datetime.datetime.now(tz=oslo)
    message.reply(now.strftime('%A %d.%m.%Y'))


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
    message.reply(
        'Daisy, Daisy, give me your answer do. Ii\'m half crazy all for the love of you. It won\'t be a stylish marriage, I can\'t afford a carriage. But you\'ll look sweet upon the seat of a bicycle built for two.')


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
    message.reply('https://github.com/cybernetisk/slackbot')


@respond_to(r'^wiki$')
@listen_to(r'^!wiki$')
def wiki_link(message):
    message.reply('https://confluence.cyb.no')


@respond_to(r'^jira$')
@listen_to(r'^!jira$')
def jira(message):
    message.reply('https://jira.cyb.no')


@respond_to(r'^.*er det kosetirdag.*$')
@listen_to(r'^.*er det kosetirsdag.*$')
@respond_to(r'^!kosetirdag$')
@listen_to(r'^!kosetirsdag$')
def social_tuesday(message):
    from datetime import date
    import calendar
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]

    if(day == 'Tuesday'):
        message.reply('Ja, det _burde_ være kosetirsdag i dag.')
    else:
        message.reply('Nei, det er tross alt ikke tirsdag.')


@respond_to(r'^.*er det mandag.*$')
@listen_to(r'^.*er det mandag.*$')
@respond_to(r'^!mandag$')
@listen_to(r'^!mandag$')
def monday(message):
    from datetime import date
    import calendar
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]

    if(day == 'Monday'):
        message.reply('Ja, men du skal vel ikke bort til RF?')
    else:
        message.reply('Nei, enda godt.')

