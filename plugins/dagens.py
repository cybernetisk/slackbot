#!/usr/bin/env python3

from slackbot.bot import respond_to, listen_to
import urllib
import json, codecs, requests
from bs4 import BeautifulSoup
from sio import Dagens



@respond_to(r'dagens$')
@respond_to(r'dagens (.*)')
@listen_to(r'!dagens$')
@listen_to(r'!dagens (.*)')
def dagens(message, cafeteria=None):
    sio = Dagens()
    if cafeteria is None:
        message.reply(sio.get_dinner_from_sio())
    elif cafeteria == 'help':
        message.reply(sio.help())
        return
    else:
        message.reply(sio.get_dinner_from_sio(cafeteria))