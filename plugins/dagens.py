#!/usr/bin/env python3

from slackbot.bot import respond_to, listen_to
import urllib
import json, codecs, requests
from bs4 import BeautifulSoup


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



class Dagens(object):
    def __init__(self):
        with open('plugins/cafeteria.json') as f:
            self.cafeterias = json.load(f)
        self.url = 'https://sio.no/mat-og-drikke/_window/mat+og+drikke+-+dagens+middag?s={}'

    def help(self):
        retstr = 'Valid cafeterias is:\n'
        for cafeteria in self.cafeterias:
            retstr += cafeteria + ' '
        return retstr

    def get_dinner_cafeteria(self, cafeteria):
        if cafeteria not in self.cafeterias:
            return 'Cafeteria not found'
        html = requests.get(self.url.format(self.cafeterias[cafeteria])).text

        soup = BeautifulSoup(html, 'html.parser')

        headers = soup.find_all('h3')
        paragraphs = soup.find_all('p')

        menu = ''

        for c, d in zip(headers, paragraphs):
            dishes = d.find_all('span')

            for dish in dishes:
                menu += '%s: %s\n' % (c.contents[0], dish.contents[0])

        return menu

    def get_dinner_from_sio(self, cafeteria=None):
        if cafeteria is None:
            return self.get_dinner_cafeteria('informatikk')
        return self.get_dinner_cafeteria(cafeteria)
