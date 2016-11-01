import urllib2

from slackbot.bot import respond_to, listen_to

from BeautifulSoup import BeautifulSoup

@listen_to(r'^.*http.')
@listen_to(r'^.*https.')
def grabber(url):
    soup = BeautifulSoup(urllib2.urlopen(url))
    message.reply("Title:")
    message.reply(soup.title.string)
