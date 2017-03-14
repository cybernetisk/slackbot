import random
import os

from slackbot.bot import respond_to, listen_to


@respond_to(r'^shodan$')
@listen_to(r'^shodan$')
def shodan(message):
    file = os.path.dirname(__file__)
    with open(os.path.join(file, 'shodan.txt')) as f:
        quotes = []
        for line in f:
            quotes.append(line)

    message.reply(quotes[random.randint(0, len(quotes))])