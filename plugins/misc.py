from slackbot.bot import respond_to, listen_to
import datetime
import calendar

@respond_to(r'dag$')
def day(message, func=None):
    message.reply(calendar.day_name[datetime.date.today().weekday()])