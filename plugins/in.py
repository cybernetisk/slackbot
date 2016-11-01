from slackbot.bot import respond_to
from plugins.util import get_from_api, get_user_from_message, semester_is_valid

base_url = 'https://in.cyb.no/api/'


def semester_to_string(semester):
    return '%s %s' % (semester['year'], semester['semester'])


def wallet_to_string(wallet):
    return '%s got %s vouchers left for %s' % (
    wallet['user']['username'], wallet['cached_balance'], semester_to_string(wallet['semester']))


@respond_to(r'^vouchers$')
@respond_to(r'^vouchers (.*)')
def vouchers(message, username=None):
    printed = False
    if username is None:
        if 'user' in message.body:
            user = get_user_from_message(message)
            username = user['name']
    wallets = get_from_api(base_url + 'voucher/wallets?user=' + username)
    if len(wallets) is 0:
        message.reply('There isn\'t any information for %s' % username)
    for wallet in wallets:
        if semester_is_valid(wallet['semester']):
            printed = True
            message.reply(wallet_to_string(wallet))
    if printed is False:
        message.reply('I can\'t find a wallet for %s this semester' % username)

