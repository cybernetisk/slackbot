from slackbot.bot import respond_to, listen_to
from slackbot_settings import EVENT_URL
from slackbot_settings import INTERN_URL as base_url
from plugins.util import get_from_api, get_user_from_message, semester_is_valid
from dateutil import parser


def semester_to_string(semester):
    return '%s %s' % (semester['year'], semester['semester'])


def wallet_to_string(wallet):
    return '%s got %s vouchers left for %s' % (
        wallet['user']['username'], wallet['cached_balance'], semester_to_string(wallet['semester']))


@respond_to(r'^vouchers$')
@respond_to(r'^vouchers (.*)')
@respond_to(r'^bong$')
@respond_to(r'^bong (.*)')
@respond_to(r'^bongs$')
@respond_to(r'^bongs (.*)')
@respond_to(r'^bonger$')
@respond_to(r'^bonger (.*)')
@listen_to(r'!vouchers$')
@listen_to(r'!vouchers (.*)')
@listen_to(r'!bong$')
@listen_to(r'!bong (.*)')
@listen_to(r'!bongs$')
@listen_to(r'!bongs (.*)')
@listen_to(r'!bonger$')
@listen_to(r'!bonger (.*)')
def vouchers(message, username=None):
    printed = False
    if username is None:
        if 'user' in message.body:
            user = get_user_from_message(message)
            username = user['name']
    wallets = get_from_api(base_url + 'voucher/wallets?user=' + username, encoding='utf8')
    for wallet in wallets:
        if semester_is_valid(wallet['semester']):
            printed = True
            message.reply(wallet_to_string(wallet))
    if printed is False:
        message.reply('I can\'t find a valid wallet for %s' % username)


def decode_event(events):
    ret = ''
    for event in events:
        time = parser.parse(event['start'])
        ret = ret + '%s: %s\n' % (event['summary'], time.strftime('%a %d.%m kl. %H:%M'))
    return ret


@respond_to(r'^events$')
@respond_to(r'^events (.*)')
@listen_to(r'!events$')
@listen_to(r'!events (.*)')
def events(message, eventtype='extern'):
    events = get_from_api(EVENT_URL, encoding='utf-8', cache=True,
                          cache_experation=600)
    if eventtype == 'intern':
        message.reply(decode_event(events['intern']))
    else:
        message.reply(decode_event(events['public']))
