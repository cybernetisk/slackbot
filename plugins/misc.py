from slackbot.bot import respond_to, listen_to
import datetime
import calendar
from pytz import timezone

@respond_to(r'dag$')
def day(message, func=None):
    oslo = timezone('Europe/Oslo')
    now = datetime.datetime.now(tz=oslo)
    message.reply(calendar.day_name[now.weekday()])

