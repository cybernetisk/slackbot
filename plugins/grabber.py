from slackbot.bot import respond_to, listen_to

import urllib

from BeautifulSoup import BeautifulSoup

@listen_to(r'^http.*')
@listen_to(r'^https.*')
def grabber(message, url=None):
    soup = BeautifulSoup(requests.get(url))
    message.reply("Title:")
    message.reply(soup.title.string)
